from telegram import ReplyKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Услуги', 'Контакты салонов'],
        ['Хочу записаться', 'Мои записи'],
    ], resize_keyboard=True)
