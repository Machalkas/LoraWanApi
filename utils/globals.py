from typing import Dict
from clients.mqtt_client import MqttClient
from database_drivers.clickHouseClient import ClickHouseWriter
from clickhouse_driver import Client


class Globals:
    def __init__(self):
        self.mqtt_client: MqttClient = None
        self.clickhouse_client: Client = None
        self.clickhouse_writers: Dict[str, ClickHouseWriter]


globals = Globals()
