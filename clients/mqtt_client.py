import asyncio
import json
from typing import Union
from gmqtt import Client
from utils import logger


class MqttClient:
    def __init__(self,
                 handler,
                 host: str,
                 port: int = 1883,
                 username: str = None,
                 password: str = None,
                 topics_to_subscribe: list = None):
        self.client = Client("LoraWAN_api_service")
        self.handler = handler
        self.host = host
        self.port = port
        self.topics_to_subscribe = topics_to_subscribe
        if username is not None:
            self.client.set_auth_credentials(username, password)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

    def subscribe(self, topics: Union[str, list], qos: int = 1):
        if isinstance(topics, str):
            topics = [topics]
        for topic in topics:
            self.client.subscribe(topic, qos)

    def on_message(self, client, topic: str, payload: bytes, qos, properties):
        if topic.endswith("response"):
            return
        payload = payload.decode('utf-8')
        result = asyncio.ensure_future(self.handler.handle_request(payload, topic), loop=self.event_loop)

    def on_connect(self, client, flags, rc, properties):
        logger.debug(f"Connect to mqtt ({self.host}:{self.port})")
        self.event_loop = asyncio.get_event_loop()
        if self.topics_to_subscribe is not None:
            self.subscribe(self.topics_to_subscribe)

    async def connect(self):
        await self.client.connect(self.host, self.port)

    async def publish(self, topic: str, payload: Union[str, dict], qos: int = 1):
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        self.client.publish(topic, payload, qos)


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
