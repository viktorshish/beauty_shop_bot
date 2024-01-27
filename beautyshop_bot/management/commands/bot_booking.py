from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from .bot_utils import method_keyboard, main_keyboard
from beautyshop_bot.db_utils import get_masters, get_master_and_timeslots, make_order, get_dates, get_free_masters


def booking_start(update, context):
    update.message.reply_text(
        "Как вас зовут? Напишите имя",
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"


def booking_surname(update, context):
    context.user_data["order"] = {"name": update.message.text}

    update.message.reply_text(
        "Напишите фамилию",
        reply_markup=ReplyKeyboardRemove()
    )
    return "surname"


def booking_method_choice(update, context):
    context.user_data["order"]["surname"] = update.message.text

    message = 'Выберите способ записи'
    update.message.reply_text(message, reply_markup=method_keyboard())
    return "booking"

def booking_method_1(update, context):
    print("Method 1", update.message.text)

def booking_method_2(update, context):
    # print("Method 2", update.message.text)
    context.user_data["order_type"] = "master"
    masters = get_masters()
    answer_message = f"У нас работают следующие мастера:\n\n"
    for master in masters:
        answer_message += f"{master['name']} {master['surname']}\n"
        answer_message += f"Услуги: {master['specialities']}\n"
        answer_message += f"\n"

    update.message.reply_text(answer_message)
    # reply_keyboard = [["1", "2", "3", "4", "5"]]
    reply_keyboard = [[f"{master['name']}" for master in masters]]
    update.message.reply_text(
        "Выберите мастера",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "booking_master"


def booking_master(update, context):
    master_name = update.message.text
    context.user_data["order"]["master"] = master_name
    timeslots = get_master_and_timeslots(master_name)

    update.message.reply_text(f"Для мастера {master_name} есть следующие записи:")
    keyboard = []
    # print(timeslots)
    answer_message = ""
    for salon, slots in timeslots.items():
        answer_message += f"В салон {salon}\n"
        # print(slots)
        for ts in slots:
            answer_message += f"{ts.day}/{ts.month} - {ts.hour}\n"
            keyboard.append([f"{salon}: {ts.day}/{ts.month} - {ts.hour}"])

    update.message.reply_text(
        answer_message,
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return "order"


# def prepare_order_master(update, context):
#     order_date = update.message.text
#     context.user_data["order"]["date"] = order_date
#
#     return "order"

def create_order(update, context):
    if context.user_data["order_type"] == "master":
        order_date = update.message.text
        context.user_data["order"]["date"] = order_date
    elif context.user_data["order_type"] == "time":
        master = update.message.text
        print(master)
        context.user_data["order"]["master"] = master



    order = {
        "client_name": context.user_data["order"]["name"],
        "client_surname": context.user_data["order"]["surname"],
        "master_name": context.user_data["order"]["master"],
        "date": context.user_data["order"]["date"],
    }
    print(order)
    order_confirmation = make_order(order)
    if order_confirmation:
        update.message.reply_text("Спасибо за заказ!", reply_markup=main_keyboard())
        return -1
    else:
        update.message.reply_text("Ошибка!", reply_markup=main_keyboard())
        return -1




def booking_method_3(update, context):
    print("Method 3", update.message.text)
    # print("Method 2", update.message.text)
    context.user_data["order_type"] = "time"

    dates = get_dates()
    reply_keyboard = [[ f"{date.day}/{date.month}" ] for date in dates]
    update.message.reply_text(
        "Выберите дату для записи:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "booking_date"

def booking_date(update, context):
    order_date = update.message.text
    context.user_data["order"]["date"] = order_date
    reply_keyboard = [[ f"{hour}:00" ] for hour in range(8, 21)]
    update.message.reply_text(
        "Выберите время для записи:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "booking_time"


def booking_time(update, context):
    order_time = update.message.text.split(":")[0]
    order_date = context.user_data["order"]["date"] + f" - {order_time}"
    print(order_date)
    context.user_data["order"]["date"] = order_date

    masters = get_free_masters(order_date)
    answer_message = f"Будут свободны следующие мастера:\n\n"
    for master in masters:
        answer_message += f"{master['name']} {master['surname']}\n"
        answer_message += f"Услуги: {master['specialities']}\n"
        answer_message += f"В салоне: {master['salon']}\n"
        answer_message += f"\n"
    update.message.reply_text(answer_message)

    reply_keyboard = [[f"{master['name']}"] for master in masters]
    update.message.reply_text(
        "Выберите мастера",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "order"

# def prepare_order_time(update, context):
#     master = update.message.text
#     print(master)
#     context.user_data["order"]["master"] = master
#
#     return "order"
