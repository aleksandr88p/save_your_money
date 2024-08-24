from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

class PurchaseState(StatesGroup):
    waiting_for_purchase = State()
    waiting_for_receipt_photo = State()
    waiting_for_spending_question = State()


# Обработчик для ручного ввода данных о покупке
async def handle_manual_input(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Пожалуйста, введите данные о покупке (например: Молоко, 150 руб, 23.08.2024).")
    await state.set_state(PurchaseState.waiting_for_purchase)

async def process_purchase(message: Message, state: FSMContext, bot: Bot):
    purchase_info = message.text
    await message.answer(f"Вы ввели следующие данные о покупке: {purchase_info}")
    await state.clear()  # Завершаем состояние

# Обработчик для ожидания фото чека
async def handle_receipt_photo(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Пожалуйста, отправьте фото чека.")
    await state.set_state(PurchaseState.waiting_for_receipt_photo)

async def process_receipt_photo(message: Message, state: FSMContext, bot: Bot):
    if message.photo:
        # Если отправлено фото
        await message.answer("Фото чека получено! Обрабатываю...")
        await state.clear()  # Завершаем состояние
    else:
        await message.answer("Пожалуйста, отправьте фото, а не текстовое сообщение.")

# Обработчик для ожидания вопроса о тратах
async def handle_spending_request(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Пожалуйста, введите вопрос о ваших тратах (например: Сколько я потратил на еду за август?).")
    await state.set_state(PurchaseState.waiting_for_spending_question)

async def process_spending_question(message: Message, state: FSMContext, bot: Bot):
    question = message.text
    await message.answer(f"Вы задали вопрос: {question}. Начинаю обработку...")
    await state.clear()  # Завершаем состояние