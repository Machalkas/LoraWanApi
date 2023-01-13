import json
from sqlalchemy.orm import Session
from deserializers import StatisticDeserializer, EnergyMeterListDeserializer
from deserializers.exceptions import BaseDeserializerException
from utils.api import Api
from utils.globals import globals
from utils import logger
from app_energy_meters.crud import update_energy_meter_list
from app_energy_meters.schemas import EnergyMeterCreateSchema
from database_clients.postgres_client import SessionLocal

mqtt_api = Api()


class MqttHandler:

    async def handle_request(self, message, topic):
        if not isinstance(message, dict):
            message = json.loads(message)
        logger.debug(f"handle {topic}")
        try:
            result = await mqtt_api.handle_request(self, message, topic)
            await globals.mqtt_client.publish(topic+"/response", result, 1)
        except BaseDeserializerException as ex:
            logger.error(f"Fail handle request {topic} -> {type(ex).__name__}: {ex}")
            await globals.mqtt_client.publish(topic+"/response", {"error": str(ex)}, 1)

    @mqtt_api.handler("device/*/save_statistic", StatisticDeserializer)
    async def save_statistic(self, message: StatisticDeserializer, topic: str):
        data = message.data.get_dict()
        globals.clickhouse_writers[message.metric].add_values(data)

    @mqtt_api.handler("device/*/get_statistic")
    async def get_statistic(self, topic: str):
        pass

    @mqtt_api.handler("device/*/update_energy_meters", EnergyMeterListDeserializer)
    async def update_energy_meters(self, message: EnergyMeterListDeserializer, topic: str):
        db = SessionLocal()
        schemas = [EnergyMeterCreateSchema(device_eui=dev.device_eui, device=dev.device)
                   for dev in message.energy_meters]
        new_energy_meters = update_energy_meter_list(db, schemas)
        kekus = [dev.to_dict() for dev in new_energy_meters]
        await globals.mqtt_client.publish(topic+"/response", kekus, 1)
