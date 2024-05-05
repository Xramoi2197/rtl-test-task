import asyncio
import logging

from aiogram import Bot, Dispatcher

import handlers
from settings import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN.get_secret_value())
dp = Dispatcher()
dp.include_router(handlers.router)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
