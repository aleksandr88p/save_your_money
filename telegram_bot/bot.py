import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv
import os

from core.handlers.command_basic import command_echo

load_dotenv()
TOKEN_TELEGRAM_BOT = os.getenv('TOKEN_TELEGRAM_BOT')


async def start():

    # Инициализация бота и диспетчера
    bot = Bot(token=TOKEN_TELEGRAM_BOT)
    dispatcher = Dispatcher()

    dispatcher.message.register(command_echo, Command(commands=['echo']))

    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())
