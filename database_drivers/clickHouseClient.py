import asyncio
from queue import Queue
import time
from typing import List, Optional
from clickhouse_driver import Client
import threading
from utils import logger

from config import CLICKHOUSE_DB_NAME, CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD


class ClickHouseStorage:
    async_loop = None
    event_loop_thread = None
    query_queue = Queue(maxsize=0)


class ClickHouseGlobals:
    def __init__(self,
                 clickhouse_client: Client,
                 child_self,
                 alias_name: str,
                 min_inserts_count: Optional[int] = None,
                 max_inserts_count: int = 100,
                 timeout_sec: int = 10,
                 clickhouse_storage: ClickHouseStorage = ClickHouseStorage()
                 ):
        self.alias_name = alias_name
        self.clickhouse_client = clickhouse_client
        self.global_vars = clickhouse_storage
        if self.global_vars.async_loop is None:
            self.global_vars.async_loop = asyncio.new_event_loop()
        if self.global_vars.event_loop_thread is None or self.global_vars.event_loop_thread.is_alive() is False:
            self.global_vars.event_loop_thread = threading.Thread(
                target=self.event_loop, args=(self.global_vars.async_loop,))
            self.global_vars.event_loop_thread.daemon = True
            self.global_vars.event_loop_thread.start()
        asyncio.ensure_future(self.scheduler(max_inserts_count, min_inserts_count,
                              timeout_sec, child_self), loop=self.global_vars.async_loop)

    def event_loop(self, loop: asyncio.AbstractEventLoop):
        asyncio.set_event_loop(loop)
        asyncio.ensure_future(self.clickhouse_query_executor(loop), loop=loop)
        loop.run_forever()

    async def clickhouse_query_executor(self, loop: asyncio.AbstractEventLoop):
        while True:
            if not self.global_vars.query_queue.empty():
                query_dict: dict = self.global_vars.query_queue.get()
                alias = query_dict.get("alias_name")
                try:
                    # TODO: catch exceptions here
                    self.clickhouse_client.execute(query_dict["query"], query_dict["values"], types_check=True)
                    inserts_count = len(query_dict["values"])
                    logger.important(f"Write to db ({inserts_count}) - {alias}")
                except Exception as e:
                    logger.error(f"Error in {alias} while try too write data do db: {e}")
            await asyncio.sleep(2)
        loop.stop()

    async def scheduler(self, max_inserts_count: int, min_inserts_count: int, timeout: int, child_self):
        timer = time.time()
        while True:
            if len(child_self.values_list) >= max_inserts_count:
                logger.info(f"Size trigger fired - {self.alias_name}")
                self.global_vars.query_queue.put({"query": child_self.query, "values": child_self.values_list})
                child_self.values_list = []  # TODO: add blocking values_list
            elif time.time()-timer >= timeout and len(child_self.values_list) >= min_inserts_count:
                logger.info(f"Timeout trigger fired - {self.alias_name}")
                self.global_vars.query_queue.put(
                    {"query": child_self.query, "values": child_self.values_list, "alias_name": child_self.alias_name})
                child_self.values_list = []
                timer = time.time()
            await asyncio.sleep(0.1)


class ClickHouseCustomClient(ClickHouseGlobals):
    def __init__(self,
                 clickhouse_client: Client,
                 create_table_query: str = None,
                 table_name: str = None,
                 values_names: list = None,
                 min_inserts_count: int = 1,
                 max_inserts_count: int = 100,
                 timeout_sec: int = 10,
                 alias_name: Optional[str] = None
                 ):
        self.clickhouse_client = clickhouse_client
        if not create_table_query and not (table_name and values_names):
            raise Exception("Must set create_table_query or table and values parameters")

        if create_table_query:
            table_name = create_table_query.split("(")[0].split()[-1]
            values_names = create_table_query.split("`")[1::2]
            clickhouse_client.execute(create_table_query)

        self.max_inserts_count = max_inserts_count
        self.query = f"INSERT INTO {table_name} ({', '.join(values_names)}) VALUES"
        self.values_names = values_names
        self.table_name = table_name
        self.alias_name = alias_name
        self.values_list: List[dict] = []
        super().__init__(clickhouse_client=clickhouse_client,
                         max_inserts_count=max_inserts_count,
                         min_inserts_count=min_inserts_count,
                         timeout_sec=timeout_sec,
                         child_self=self,
                         alias_name=alias_name if alias_name is not None else table_name)

    def add_values(self, values: dict):  # TODO: add sql injection security
        if type(values) is dict and set([*values]) != set(self.values_names):
            raise Exception("Insert query values do not match")
        self.values_list.append(values)

    def get(self, columns: list, filter_sql_query: str = None, get_from_buffer: bool = True):
        sql_query = f"SELECT {', '.join(columns)} FROM {self.table_name}"
        if filter_sql_query:
            sql_query += f" WHERE {filter_sql_query};"
        data_from_db = self.clickhouse_client.execute(sql_query)
        if get_from_buffer:  # TODO: add filters
            data_from_buffer = []
            for record in self.values_list:
                record: dict = [(key, record[key]) for key in columns if key in record]
                data_from_buffer.append(tuple(val for key, val in record if key in columns))
            return data_from_db+data_from_buffer
        return data_from_db


if __name__ == "__main__":
    from datetime import datetime
    clickhouse_client = Client(host=CLICKHOUSE_HOST,
                               port=CLICKHOUSE_PORT,
                               user=CLICKHOUSE_USER)
    test = ClickHouseCustomClient(
        clickhouse_client, f"CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB_NAME}.logs (`datetime` DateTime, `tags` String, `fields` String) ENGINE=StripeLog()", timeout_sec=10000, max_inserts_count=10000)
    # test2 = ClickHouseWriter(clickhouse_client, table_name=f"{CLICKHOUSE_DB_NAME}.logs", values_names=[
    #                          "datetime", "tags", "fields"], timeout_sec=30)

    for i in range(1000):
        test.add_values({"datetime": datetime.now(), "tags": f"tag_3", "fields": f"field_3.{i}"})

    # for i in range(1000, 3000):
    #     test2.add_values({"datetime": datetime.now(), "tags": f"tag_2", "fields": f"field_2.{i}"})
    # time.sleep(10)

    # for i in range(3000, 3010):
    #     test.add_values({"datetime": datetime.now(), "tags": f"tag_1", "fields": f"field_1.{i}"})

    # count = 3010
    # while True:
    #     test.add_values({"datetime": datetime.now(), "tags": f"tag_1", "fields": f"field_1.{count}"})
    #     test2.add_values({"datetime": datetime.now(), "tags": f"tag_2", "fields": f"field_2.{count}"})
    #     count += 1
    #     time.sleep(0.2)

    print(test.get(["fields", "tags"], "'tags'!='1235'", get_from_buffer=True))


"""
docker run -d -p 8123:8123 -p 9000:9000 -v /mnt/d/clickhouse:/var/lib/clickhouse --name clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server
"""
