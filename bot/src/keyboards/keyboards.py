from aiogram.types import KeyboardButton, ReplyKeyboardMarkup





keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рестораны')
        ]
    ],
    resize_keyboard=True
)

def get_category_for_new_establishment():
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='ресторан'), KeyboardButton(text='кафе')]
        ],
        resize_keyboard=True
    )
    return keyboard