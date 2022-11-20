import asyncio
from fastapi import FastAPI
from clients.mqtt_client import MqttClient
from utils.globals import globals
import config

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

globals.mqtt_client = MqttClient(config.MQTT_HOST, config.MQTT_PORT, config.MQTT_USERNAME, config.MQTT_PASSWORD,
                                 config.MQTT_TOPICS_TO_SUBSCRIBE)

event_loop = asyncio.new_event_loop()
event_loop.create_task(globals.mqtt_client.connect())
event_loop.run_forever()
