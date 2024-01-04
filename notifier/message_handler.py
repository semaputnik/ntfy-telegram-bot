import json
import logging

from telegram._bot import BT

from notifier.message import Message
from notifier.templates import _get_template_env


class MessageHandler:
    def __init__(self, bot: BT, chat_id: str):
        self.bot: BT = bot
        self.chat_id: str = chat_id
        self.template = _get_template_env().get_template("message_template.j2")

    async def handle(self, raw_message: str):
        logging.info(f"Received message: {raw_message}")
        message: Message = Message(**(json.loads(raw_message)))
        await self.bot.send_message(self.chat_id, text=self.parse(message), parse_mode="HTML")

    def parse(self, message: Message) -> str:
        rendered = self.template.render(**message.model_dump()).replace("<br>", "\n")
        return rendered
