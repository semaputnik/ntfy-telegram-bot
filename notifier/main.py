import asyncio
import logging
from logging import getLogger
from logging.config import fileConfig
from warnings import filterwarnings

import websockets
from telegram.ext import ApplicationBuilder
from telegram.warnings import PTBUserWarning

from notifier.message_handler import MessageHandler
from notifier.settings import Settings
from notifier.topic_handler import TopicHandler

settings = Settings()

fileConfig(settings.LOGGING_FILE_PATH, defaults={'logfilename': f"{settings.LOGS_DIR}/notifier.log"})
logger = getLogger(__name__)
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)


async def subscribe(topics, bot):
    loop = asyncio.get_event_loop()
    tasks = []
    # create a task for each URL
    for topic in topics:
        message_handler: MessageHandler = MessageHandler(bot, settings.chat_id)
        topic_handler: TopicHandler = TopicHandler(topic, settings.base_url, message_handler)
        task = loop.create_task(topic_handler.handle())
        tasks.append(task)
    # run all tasks in parallel
    await asyncio.gather(*tasks)


async def main():
    application = ApplicationBuilder() \
        .token(settings.token) \
        .build()

    bot = application.bot

    logging.info("Application started")
    await bot.send_message(settings.chat_id, "Application started \n#notifier_restart")

    await subscribe(settings.topics, bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
