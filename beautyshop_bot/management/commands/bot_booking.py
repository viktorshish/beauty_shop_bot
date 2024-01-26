from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from .bot_utils import method_keyboard
from beautyshop_bot.db_utils import get_masters


def booking_start(update, context):
    update.message.reply_text(
        "Как вас зовут? Напишите имя",
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"


def booking_surname(update, context):
    context.user_data["anketa"] = {"name": update.message.text}

    update.message.reply_text(
        "Напишите фамилию",
        reply_markup=ReplyKeyboardRemove()
    )
    return "surname"


def booking_method_choice(update, context):
    context.user_data["anketa"]["surname"] = update.message.text

    message = 'Выберите способ записи'
    update.message.reply_text(message, reply_markup=method_keyboard())
    return "booking"

def booking_method_1(update, context):
    print("Method 1", update.message.text)

def booking_method_2(update, context):
    # print("Method 2", update.message.text)
    masters = get_masters()
    answer_message = f"У нас работают следующие мастера:\n\n"
    for master in masters:
        answer_message += f"{master['name']} {master['surname']}\n"
        answer_message += f"Услуги: {master['specialities']}\n"
        answer_message += f"\n"

    update.message.reply_text(answer_message)
    # reply_keyboard = [["1", "2", "3", "4", "5"]]
    reply_keyboard = [[ f"{master.name}" for master in masters]]
    update.message.reply_text(
        "Выберите мастера",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "booking_master"

def booking_master(update, context):
    master_name = update.message.text



def booking_method_3(update, context):
    print("Method 3", update.message.text)


