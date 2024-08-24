import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv
import os

from core.handlers.command_basic import command_echo, command_start
from core.handlers.user_input import handle_receipt_photo, handle_manual_input, handle_spending_request, process_purchase, process_receipt_photo, process_spending_question
from core.handlers.user_input import PurchaseState
from core.buttons import get_main_menu

load_dotenv()
TOKEN_TELEGRAM_BOT = os.getenv('TOKEN_TELEGRAM_BOT')


async def start():

    # Инициализация бота и диспетчера
    bot = Bot(token=TOKEN_TELEGRAM_BOT)
    dispatcher = Dispatcher()

    dispatcher.message.register(command_start, Command(commands=['start']))
    dispatcher.message.register(command_echo, Command(commands=['echo']))

    # Регистрация обработчиков для текстовых команд-кнопок
    dispatcher.message.register(handle_receipt_photo, lambda message: message.text == '📸 Отправить чек')
    dispatcher.message.register(handle_manual_input, lambda message: message.text == '✍️ Ввести покупку вручную')
    dispatcher.message.register(handle_spending_request, lambda message: message.text == '📊 Запросить информацию о тратах')


    dispatcher.message.register(process_purchase, PurchaseState.waiting_for_purchase)
    dispatcher.message.register(process_receipt_photo, PurchaseState.waiting_for_receipt_photo)
    dispatcher.message.register(process_spending_question, PurchaseState.waiting_for_spending_question)


    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())
