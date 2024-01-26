from telegram import ReplyKeyboardRemove


def booking_start(update, context):
    update.message.reply_text(
        "Как вас зовут? Напишите имя",
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"


def booking_surname(update, context):

    update.message.reply_text(
        "Как вас зовут? Напишите имя",
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"
