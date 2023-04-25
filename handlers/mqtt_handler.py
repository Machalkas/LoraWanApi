import json
from sqlalchemy.orm import Session
from prometheus_client import Summary
from prometheus_async.aio import time
from deserializers import StatisticDeserializer, EnergyMeterListDeserializer
from deserializers.exceptions import BaseDeserializerException
from utils.api import Api
from utils.globals import globals
from utils import logger
from app_energy_meters.crud import update_energy_meter_list
from app_energy_meters.schemas import EnergyMeterCreateSchema
from database_clients.postgres_client import SessionLocal

mqtt_api = Api()
summary = Summary("mqtt_handler_time", "How long request handler run")


class MqttHandler:

    @time(summary)
    async def handle_request(self, message, topic):
        if not isinstance(message, dict):
            message = json.loads(message)
        logger.debug(f"handle {topic}")
        try:
            result = await mqtt_api.handle_request(self, message, topic)
            await globals.mqtt_client.publish(topic+"/response", result)
        except BaseDeserializerException as ex:
            logger.error(f"Fail handle request {topic} -> {type(ex).__name__}: {ex}")
            await globals.mqtt_client.publish(topic+"/response", {"error": str(ex)})

    @mqtt_api.handler("device/save_statistic", StatisticDeserializer)
    async def save_statistic(self, message: StatisticDeserializer, topic: str):
        data = message.data.get_dict()
        globals.clickhouse_writers[message.metric].add_values(data)

    @mqtt_api.handler("device/get_statistic")
    async def get_statistic(self, topic: str):
        pass

    @mqtt_api.handler("device/update_energy_meters", EnergyMeterListDeserializer)
    async def update_energy_meters(self, message: EnergyMeterListDeserializer, topic: str):
        db = SessionLocal()
        schemas = [EnergyMeterCreateSchema(device_eui=dev.device_eui, device=dev.device)
                   for dev in message.energy_meters]
        new_energy_meters = update_energy_meter_list(db, schemas)
        kekus = [dev.to_dict() for dev in new_energy_meters]
        await globals.mqtt_client.publish(topic+"/response", kekus)
    
    @mqtt_api.not_found_handler()
    async def not_found(self, topic: str):
        logger.warning(f"Handler for topic {topic} not found")
        await globals.mqtt_client.publish(topic+"/response", {"error": "handler not found"})
