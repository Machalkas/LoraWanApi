
import json
from typing import Union
from os.path import normpath


class Api:
    def __init__(self) -> None:
        self.handlers = {}

    def handler(self, topic: str):
        assert topic not in self.handlers, f"Handler with topic \"{topic}\" already exists"

        def wrapper(handler):
            self.handler[normpath(topic)] = handler
            return handler
        return wrapper

    async def handle_request(self, handler_self, message: Union[str, dict], topic: str):
        topic = normpath(topic)
        if isinstance(message, str):
            message = json.loads(message)
        handler = self.handlers.get(topic)
        if handler is None:
            return None
        return await handler(handler_self, message, topic)
        
        
