import logging

import websockets

from notifier.message_handler import MessageHandler


class TopicHandler:
    def __init__(self, topic: str, base_url: str, message_handler: MessageHandler):
        logging.info(f"Subscribing to {base_url.format(topic)}")
        self.url = base_url.format(topic)
        self.message_handler = message_handler

    async def handle(self):
        async with websockets.connect(self.url) as ws:
            while True:
                msg = await ws.recv()
                await self.message_handler.handle(msg)