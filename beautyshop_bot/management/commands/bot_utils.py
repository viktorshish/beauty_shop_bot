from telegram import ReplyKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Услуги', 'Контакты'],
        ['Хочу записаться', 'Мои записи'],
    ], resize_keyboard=True)

