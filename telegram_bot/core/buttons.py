from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    '''
    Функция для создания основного меню с кнопками
    '''
    # Определяем кнопки
    photo_button = KeyboardButton(text='📸 Отправить чек')
    manual_input_button = KeyboardButton(text='✍️ Ввести покупку вручную')
    spending_request_button = KeyboardButton(text='📊 Запросить информацию о тратах')

    # Создаем клавиатуру с необходимой структурой
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [photo_button],
            [manual_input_button],
            [spending_request_button]
        ],
        resize_keyboard=True
    )

    return keyboard
