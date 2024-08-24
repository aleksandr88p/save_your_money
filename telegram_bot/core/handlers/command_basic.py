from aiogram import Bot
from aiogram.types import Message
from aiogram.enums import ParseMode


async def command_echo(message: Message, bot: Bot):
    print(message)
    print('*******************')
    text = message.text.split("/echo")[1]
    await message.answer(text=f'{text}')
