from telegram import ReplyKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Услуги', 'Контакты'],
        ['Хочу записаться', 'Мои записи'],
    ], resize_keyboard=True)


def method_keyboard():
    return ReplyKeyboardMarkup([
        ['В салон', 'К мастеру', 'На время'],
    ], resize_keyboard=True)
