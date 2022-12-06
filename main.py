import asyncio
from fastapi import FastAPI
from clients.mqtt_client import MqttClient
from clickhouse_driver import Client
from database_clients.click_house_client import ClickHouseCustomClient
from handlers.mqtt_handler import MqttHandler
from utils.globals import globals
import config
from app_power_monitors.view import router as power_monitors_router

app = FastAPI()
app.include_router(power_monitors_router)
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
