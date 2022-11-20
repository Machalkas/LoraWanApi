
import json
from deserializers import StatisticDeserializer
from utils.api import Api
from utils.globals import globals
from utils import logger

mqtt_api = Api()


class MqttHandler:

    async def handle_request(self, message, topic):
        if not isinstance(message, dict):
            message = json.loads(message)
        logger.debug(f"handle {topic}")
        result = await mqtt_api.handle_request(self, message, topic)
        await globals.mqtt_client.publish(topic+"/response", result, 1)

    @mqtt_api.handler("device/*/save_statistic", StatisticDeserializer)
    async def save_statistic(self, message: StatisticDeserializer, topic: str):
        data = message.data.get_dict()
        globals.clickhouse_writers[message.type].add_values(data)
        return {"kekus": "kkk"}

    @mqtt_api.handler("device/*get_statistic")
    async def get_statistic(self, topic: str):
        pass