from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import Union
from config import DT_FORMAT
from deserializers.exceptions import DeserializerKeyError, DeserializerValueError, ShittyError


def catch_key_error(func):
    def wrapper(self, *args, **kargs):
        try:
            return func(self, *args, **kargs)
        except KeyError as ex:
            raise DeserializerKeyError(ex)
        except ValueError as ex:
            raise DeserializerValueError(ex)
        except Exception as ex:
            raise ShittyError(ex)
            
    return wrapper


class BaseDeserializer(ABC):
    def __init__(self, message: Union[str, dict]) -> None:
        if isinstance(message, str):
            message = json.loads(message)
        self.deserialize(message)

    @abstractmethod
    def deserialize(self, message: dict):
        pass

    def get_dict(self, ignore_key: list = None) -> dict:
        raw_dict = self.__dict__
        if not isinstance(ignore_key, list):
            return raw_dict
        for key in ignore_key:
            raw_dict.pop(key)
        return raw_dict


class PowerDataDeserializer(BaseDeserializer):
    @catch_key_error
    def deserialize(self, message: dict):
        self.datetime: datetime = datetime.strptime(message["datetime"], DT_FORMAT)
        self.counter: int = int(message["counter"])
        self.phase_a: float = float(message["phase_a"])
        self.phase_b: float = float(message["phase_b"])
        self.phase_c: float = float(message["phase_c"])
        self.total: float = float(message["total"])


class TrafficDataDeserializer(BaseDeserializer):
    @catch_key_error
    def deserialize(self, message: dict):
        self.datetime: datetime = datetime.strptime(message["datetime"], DT_FORMAT)
        self.counter: int = int(message["counter"])
        self.traffic_plan_1: float = float(message["traffic_plan_1"])
        self.traffic_plan_2: float = float(message["traffic_plan_2"])
        self.traffic_plan_3: float = float(message["traffic_plan_3"])
        self.traffic_plan_4: float = float(message["traffic_plan_4"])
        self.current_traffic: int = int(message["current_traffic"])
        self.total: float = float(message["total"])


class StatisticDeserializer(BaseDeserializer):
    statistic_metrics = {"power": PowerDataDeserializer, "traffic": TrafficDataDeserializer}

    @catch_key_error
    def deserialize(self, message: dict):
        self.metric: str = message["metric"]
        self.data: BaseDeserializer = None
        des = self.statistic_metrics.get(self.metric)
        if des is None:
            raise DeserializerValueError(f"unknown type \"{self.metric}\"")
        self.data = des(message)


class EnergyMeterDeserializer(BaseDeserializer):
    @catch_key_error
    def deserialize(self, message: dict):
        self.device_eui: str = message["device_eui"]
        self.device: str = message["device"]


class EnergyMeterListDeserializer(BaseDeserializer):
    @catch_key_error
    def deserialize(self, message: dict):
        self.energy_meters: list[EnergyMeterDeserializer] = [EnergyMeterDeserializer(dev) for dev in message]
