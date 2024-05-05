import asyncio
import logging

from aiogram import Bot, Dispatcher

import handlers
from db.query import SampleQuery
from settings import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN.get_secret_value())
dp = Dispatcher()
dp.include_router(handlers.router)


async def main() -> None:
    uri = f"mongodb://{config.MONGO_USER}:{config.MONGO_PASSWORD.get_secret_value()}@{config.MONGO_HOST}/"
    query = SampleQuery(uri, config.DB_NAME, config.COLLECTION_NAME)
    await dp.start_polling(bot, query=query)


if __name__ == "__main__":
    asyncio.run(main())
