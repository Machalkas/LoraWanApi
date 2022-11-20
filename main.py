import asyncio
from fastapi import FastAPI
from clients.mqtt_client import MqttClient
from clickhouse_driver import Client
from database_drivers.clickHouseClient import ClickHouseWriter
from utils.globals import globals
import config

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

globals.mqtt_client = MqttClient(config.MQTT_HOST, config.MQTT_PORT, config.MQTT_USERNAME, config.MQTT_PASSWORD,
                                 config.MQTT_TOPICS_TO_SUBSCRIBE)

globals.clickhouse_client = Client(host=config.CLICKHOUSE_HOST,
                                   port=config.CLICKHOUSE_PORT,
                                   user=config.CLICKHOUSE_USER)
globals.clickhouse_writers["power"] = ClickHouseWriter(globals.clickhouse_client, config.POWER_TABLE_QUERY,
                                                       max_inserts_count=config.CLICKHOUSE_MAX_COUNT,
                                                       timeout_sec=config.CLICKHOUSE_TIMEOUT)
globals.clickhouse_writers["traffic"] = ClickHouseWriter(globals.clickhouse_client, config.TRAFFIC_TABLE_QUERY,
                                                         max_inserts_count=config.CLICKHOUSE_MAX_COUNT,
                                                         timeout_sec=config.CLICKHOUSE_TIMEOUT)
event_loop = asyncio.new_event_loop()
event_loop.create_task(globals.mqtt_client.connect())
event_loop.run_forever()
