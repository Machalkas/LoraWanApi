from clients.mqtt_client import MqttClient
from database_drivers.clickHouseClient import ClickHouseWriter


class Globals:
    def __init__(self):
        self.mqtt_client: MqttClient = None
        self.clickhouse_writer: ClickHouseWriter = None


globals = Globals()