import asyncio
import json
from typing import Union

from asyncio_mqtt import Client
from asyncio_mqtt.client import Topic
from asyncio_mqtt.error import MqttError
from utils import logger
# from handlers.mqtt_handler import MqttHandler

class MqttClient:
    def __init__(self,
                 handler,
                 host: str,
                 port: int = 1883,
                 username: str = None,
                 password: str = None,
                 topics_to_subscribe: list = None):
        self.handler = handler
        self.host = host
        self.port = port
        self.topics_to_subscribe = topics_to_subscribe
        self.username = username
        self.password = password
        self.client = Client(hostname=host, port=port, username=username, password=password, client_id="LoraWAN_api_service")
        # self.client.on_message = self.on_message
        # self.client.on_connect = self.on_connect
        # self.client.on_disconnect = self.on_disconnect
        # self.client.on_subscribe = self.on_subscribe
        # self.client.on_unsubscribe = self.on_unsubscribe
        self.semaphore = asyncio.Semaphore(1000)

    async def subscribe(self, client: Client, topics: Union[str, list], qos: int = 1):
        if topics is None:
            return
        if isinstance(topics, str):
            topics = [topics]
        for topic in topics:
            await client.subscribe(topic, qos)
        logger.info(f"subscribe to topics: {topics}")

    # def on_message(self, client, topic: str, payload: bytes, qos, properties):
    #     if topic.endswith("response"):
    #         return
    #     payload = payload.decode('utf-8')
    #     result = asyncio.ensure_future(self.handle_message(self.handler.handle_request, (payload, topic), self.semaphore), loop=self.event_loop)

    # def on_connect(self, client, flags, rc, properties):
    #     logger.info(f"Connect to mqtt broker ({self.host}:{self.port})")
    #     self.event_loop = asyncio.get_event_loop()
    #     if self.topics_to_subscribe is not None:
    #         self.subscribe(self.topics_to_subscribe)

    # def on_disconnect(self, *args, **kwargs):
    #     logger.warning(f"Disconnect from mqtt broker ({self.host}:{self.port})")

    # def on_subscribe(self, client: Client, mid, qos, properties):
    #     topic = client.get_subscriptions_by_mid(mid)
    #     logger.debug(f"Subscribe to topic '{topic[0].topic}'")

    # def on_unsubscribe(self, client: Client, mid, qos, properties):
    #     topic = client.get_subscriptions_by_mid(mid)
    #     logger.debug(f"Unsubscribe from topic '{topic}'")

    async def handle_message(self, message: dict | str | bytes, topic: Topic):
        # async with self.semaphore:
        await self.semaphore.acquire()
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        if message and not topic.value.endswith("response"):
            await self.handler.handle_request(message, topic.value)
        self.semaphore.release()

    async def connect(self):
        while True:
            try:
                async with self.client as client:
                    await self.subscribe(client, self.topics_to_subscribe)
                    async with client.messages() as messages:
                        async for message in messages:
                            async with self.semaphore:
                                asyncio.create_task(self.handle_message(message.payload, message.topic))
            except MqttError:
                logger.error("MqttError")
                await asyncio.sleep(2)

        # try:
        #     await self.client.connect(self.host, self.port)
        # except Exception as ex:
        #     logger.error(f"Fail to connect to mqtt: {ex}")
        #     await self.client.disconnect()
        #     await asyncio.sleep(3)
        #     await self.connect()

    async def publish(self, topic: str, payload: Union[str, dict], qos: int = 1):
        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload)
        await self.client.publish(topic=topic, payload=payload, qos=qos)


if __name__ == "__main__":
    async def test(m: MqttClient):
        while m.client.is_connected is False:
            await asyncio.sleep(1)
        m.subscribe("test")
        print("publish")
        await m.publish("test", "kek")
    m = MqttClient("localhost", 1884, "test", "test")
    loop = asyncio.new_event_loop()
    loop.create_task(m.connect())
    loop.create_task(test(m))
    loop.run_forever()
