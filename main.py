import asyncio
from datetime import datetime
from fastapi import FastAPI, HTTPException
from clients.mqtt_client import MqttClient
from clickhouse_driver import Client
from database_drivers.clickHouseClient import ClickHouseCustomClient
from handlers.mqtt_handler import MqttHandler
from utils.globals import globals
import config

app = FastAPI()


@app.get("/power_monitor/get_statistic/{counter_id}")
async def get_statistic(counter_id: int, metric: str, from_dt: datetime = None, to_dt: datetime = None):
    ch_writer = globals.clickhouse_writers.get(metric)
    if ch_writer is None:
        raise HTTPException(404, f"Metric {metric} not found")
    filter_query = f"`counter` = {counter_id}"
    if from_dt:
        filter_query += f" and `datetime` > '{from_dt}'"
    if to_dt:
        filter_query += f" and `datetime` <= '{to_dt}'"
    response = ch_writer.get(filter_sql_query=filter_query, order_by="datetime")
    return response


globals.mqtt_handler = MqttHandler()
globals.mqtt_client = MqttClient(globals.mqtt_handler, config.MQTT_HOST, config.MQTT_PORT, config.MQTT_USERNAME,
                                 config.MQTT_PASSWORD,
                                 config.MQTT_TOPICS_TO_SUBSCRIBE)
globals.clickhouse_client = Client(host=config.CLICKHOUSE_HOST,
                                   port=config.CLICKHOUSE_PORT,
                                   user=config.CLICKHOUSE_USER)
globals.clickhouse_writers["power"] = ClickHouseCustomClient(globals.clickhouse_client, config.POWER_TABLE_QUERY,
                                                             max_inserts_count=config.CLICKHOUSE_MAX_COUNT,
                                                             timeout_sec=config.CLICKHOUSE_TIMEOUT)
globals.clickhouse_writers["traffic"] = ClickHouseCustomClient(globals.clickhouse_client, config.TRAFFIC_TABLE_QUERY,
                                                               max_inserts_count=config.CLICKHOUSE_MAX_COUNT,
                                                               timeout_sec=config.CLICKHOUSE_TIMEOUT)
event_loop = asyncio.get_event_loop()
event_loop.create_task(globals.mqtt_client.connect())
# event_loop.run_forever()
