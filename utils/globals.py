from typing import Dict
from clients.mqtt_client import MqttClient
# from handlers.mqtt_handler import MqttHandler
from database_drivers.clickHouseClient import ClickHouseCustomClient
from clickhouse_driver import Client


class Globals:
    def __init__(self):
        self.mqtt_client: MqttClient = None
        self.mqtt_handler = None
        self.clickhouse_client: Client = None
        self.clickhouse_writers: Dict[str, ClickHouseCustomClient] = {}


globals = Globals()
