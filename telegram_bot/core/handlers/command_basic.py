from aiogram import Bot
from aiogram.types import Message
from aiogram.enums import ParseMode
from ..buttons import get_main_menu


async def command_start(message: Message, bot: Bot):
    '''
    func for say hello
    :param message:
    :param bot:
    :return:
    '''
    text = "Привет! Я помогу тебе следить за твоими финансами."
    await message.answer(text=text, reply_markup=get_main_menu())


async def command_echo(message: Message, bot: Bot):
    '''
    just for test the bot
    :param message:
    :param bot:
    :return:
    '''
    text = message.text.split("/echo")[1]
    await message.answer(text=f'{text}')
