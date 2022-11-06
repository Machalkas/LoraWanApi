
from utils.api import Api

mqtt_api = Api()


class MqttHandler:

    @mqtt_api.handler("device/*/save_statistic")
    async def save_statistic(self, message: dict):
        pass

    @mqtt_api.handler("device/*get_statistic")
    async def get_statistic(self, message: dict):
        pass