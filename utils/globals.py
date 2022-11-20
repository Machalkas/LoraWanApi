from typing import Dict
from clients.mqtt_client import MqttClient
from database_drivers.clickHouseClient import ClickHouseCustomClient
from clickhouse_driver import Client


class Globals:
    def __init__(self):
        self.mqtt_client: MqttClient = None
        self.clickhouse_client: Client = None
        self.clickhouse_writers: Dict[str, ClickHouseCustomClient]


globals = Globals()
