import asyncio
import logging
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from os import getenv
from codes.handlers.commands import router

load_dotenv()
token = getenv("TOKEN")

dp = Dispatcher()

dp.include_router(router)

async def main():
    bot = Bot(token=token)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('Start...')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot off!')