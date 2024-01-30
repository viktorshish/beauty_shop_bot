from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from .bot_utils import method_keyboard, main_keyboard
from beautyshop_bot.db_utils import get_masters, get_master_and_timeslots, make_order, get_dates, get_free_masters, \
    check_if_user_exists, get_salon_contacts, get_closest_salon, get_masters_by_salon


def booking_start(update, context):
    chat_id = update.message.chat_id
    client = check_if_user_exists(chat_id)
    if client:
        context.user_data["order"] = {
            "name": client["client_name"],
            "surname": client["client_surname"],
            "phone": client["phone"],
            "telegram_chat_id": client["telegram_chat_id"],
            "telegram_nickname": client["telegram_nickname"],
        }
        message = 'Выберите способ записи'
        update.message.reply_text(message, reply_markup=method_keyboard())
        return "booking"

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


def booking_phone(update, context):
    context.user_data["order"]["surname"] = update.message.text

    update.message.reply_text(
        "Напишите телефон",
        reply_markup=ReplyKeyboardRemove()
    )
    return "phone"


def booking_method_choice(update, context):
    context.user_data["order"]["phone"] = update.message.text
    context.user_data["order"]["telegram_nickname"] = update.message.from_user['username']
    context.user_data["order"]["telegram_chat_id"] = update.message.from_user['id']

    message = 'Выберите способ записи'
    update.message.reply_text(message, reply_markup=method_keyboard())
    return "booking"

def booking_method_1(update, context):
    # print("Method 1", update.message.text)
    context.user_data["order_type"] = "salon"
    contacts = get_salon_contacts()

    answer_message = f"У нас есть следующие салоны:\n\n"
    for salon in contacts:
        answer_message += f"Салон: {salon['name']}\n"
        answer_message += f"Адрес: {salon['address']}\n"
        answer_message += f"Телефон: {salon['phone']}\n"
        answer_message += f"\n"
    reply_keyboard = [[f"{salon['name']}"] for salon in contacts]

    answer_message += "Мы так же можем порекомендовать Вам близжайши салон, если вы поделитесь своей геолокацией"

    update.message.reply_text(answer_message)

    update.message.reply_text(
        "Выберите салон",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "chose_salon"

def booking_gave_location(update, context):
    if update.message.location:
        context.user_data["location"] = update.message.location

        closest_salon = get_closest_salon(update.message.location)
        context.user_data["order"]["salon"] = closest_salon.name
        update.message.reply_text(f"Близжайший салон - {closest_salon.name}, по адресу {closest_salon.address}")
    else:
        context.user_data["order"]["salon"] = update.message.text

    # print("Gave location function")
    # print(context.user_data["order"]["salon"])
    masters = get_masters_by_salon(context.user_data["order"]["salon"])
    # print(masters)


    # keyboard = []
    answer_message = "В этом салоне работают следующие мастера\n"

    for master in masters:
        answer_message += f"{master['name']} {master['surname']}\n"
        answer_message += f"Услуги: {master['specialities']}\n"
        answer_message += f"\n"

    update.message.reply_text(answer_message)
    # reply_keyboard = [["1", "2", "3", "4", "5"]]
    reply_keyboard = [[f"{master['name']}"] for master in masters]
    update.message.reply_text(
        "Выберите мастера",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return "chose_master"


def booking_get_dates_for_salon(update, context):
    master_name = update.message.text
    context.user_data["order"]["master"] = master_name
    timeslots = get_master_and_timeslots(master_name)

    update.message.reply_text(f"Для мастера {master_name} есть следующие записи:")
    keyboard = []
    # print(timeslots)
    answer_message = ""
    for salon, slots in timeslots.items():
        if salon == context.user_data["order"]["salon"]:
            # answer_message += f"В салон {salon}\n"
            # print(slots)
            temp_keyboard = []
            for count, ts in enumerate(slots):
                answer_message += f"{ts.day}/{ts.month} - {ts.hour} часов\n"
                temp_keyboard.append(f"{salon}: {ts.day}/{ts.month} - {ts.hour} часов")
                # if count % 4 == 0:
                #     answer_message += "\n"
                if count % 2 == 0 or count >= len(slots) - 1:
                    keyboard.append(temp_keyboard)
                    temp_keyboard = []
    # print(keyboard)

    update.message.reply_text(
        answer_message,
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return "order"



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
    reply_keyboard = [[f"{master['name']}"] for master in masters]
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
    temp_keyboard = []
    for salon, slots in timeslots.items():
        answer_message += f"В салон {salon}\n"
        # print(slots)
        temp_keyboard = []
        for count, ts in enumerate(slots):
            answer_message += f"{ts.day}/{ts.month} - {ts.hour} часов\t"
            temp_keyboard.append(f"{salon}: {ts.day}/{ts.month} - {ts.hour} часов")
            if count % 4 == 0:
                answer_message += "\n"
            if count % 2 == 0 or count >= len(slots) - 1:
                keyboard.append(temp_keyboard)
                temp_keyboard = []

    # print(keyboard)

    update.message.reply_text(
        answer_message,
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return "order"


def create_order(update, context):
    if context.user_data["order_type"] == "master":
        order_date = update.message.text.split(':')[1].strip("часов").strip()
        context.user_data["order"]["date"] = order_date
    elif context.user_data["order_type"] == "time":
        master = update.message.text
        # print(master)
        context.user_data["order"]["master"] = master
    elif context.user_data["order_type"] == "salon":
        order_date = update.message.text.split(':')[1].strip("часов").strip()
        # print(master)
        context.user_data["order"]["date"] = order_date



    order = {
        "client_name": context.user_data["order"]["name"],
        "client_surname": context.user_data["order"]["surname"],

        "phone": context.user_data["order"]["phone"],
        "telegram_chat_id": context.user_data["order"]["telegram_chat_id"],
        "telegram_nickname": context.user_data["order"]["telegram_nickname"],

        "master_name": context.user_data["order"]["master"],
        "date": context.user_data["order"]["date"],
    }
    # print(order)
    order_confirmation = make_order(order)
    if order_confirmation:
        update.message.reply_text("Спасибо за заказ!", reply_markup=main_keyboard())
        return -1
    else:
        update.message.reply_text("Ошибка!", reply_markup=main_keyboard())
        return -1


def booking_method_3(update, context):
    # print("Method 3", update.message.text)
    # print("Method 2", update.message.text)
    context.user_data["order_type"] = "time"

    dates = get_dates()

    inline_keyboard = [
        [
            InlineKeyboardButton(f"{dates[i + j].day}/{dates[i + j].month}",
                                 callback_data=f"date|{dates[i + j].day}/{dates[i + j].month}")
            for j in range(0, 5)
        ]
        for i in range(0, len(dates), 5)
    ]

    # reply_keyboard = [[ f"{date.day}/{date.month}" ] for date in dates]


    update.message.reply_text(
        "Выберите дату для записи:",
        reply_markup=InlineKeyboardMarkup(
                inline_keyboard
            )
        )

    return "booking_date"

def booking_method_4(update, context):
        update.message.reply_text("Для записи , позвоните на номер нашему администратору 📱📱📱 214143", reply_markup=main_keyboard())
        return -1

def booking_date(update, context):
    update.callback_query.answer()

    order_date = update.callback_query.data.split("|")[-1]
    context.user_data["order"]["date"] = order_date
    # reply_keyboard = [[ f"{hour + i}:00" for i in range(4) ] for hour in range(8, 21, 4)]
    inline_keyboard = [
        [
            InlineKeyboardButton(f"{hour + i}:00",
                                 callback_data=f"time|{hour + i}:00")
            for i in range(0, 5)
        ]
        for hour in range(8, 21, 4)
    ]

    update.callback_query.message.edit_text(
        "Выберите время для записи:",
        # reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard
        )
    )
    return "booking_time"


def booking_time(update, context):
    update.callback_query.answer()
    order_time = update.callback_query.data.split("|")[-1].split(":")[0]
    # context.user_data["order"]["date"] = order_date

    # order_time = update.message.text.split(":")[0]
    order_date = context.user_data["order"]["date"] + f" - {order_time}"
    # print(order_date)
    context.user_data["order"]["date"] = order_date

    masters = get_free_masters(order_date)
    answer_message = f"Будут свободны следующие мастера:\n\n"
    if not masters:
        answer_message += f"К сожалению, все мастера на это время заняты"
        update.effective_chat.send_message(answer_message, reply_markup=main_keyboard())
        return -1
    for master in masters:
        answer_message += f"{master['name']} {master['surname']}\n"
        answer_message += f"Услуги: {master['specialities']}\n"
        answer_message += f"В салоне: {master['salon']}\n"
        answer_message += f"\n"
    update.effective_chat.send_message(answer_message)

    reply_keyboard = [[f"{master['name']}"] for master in masters]
    update.effective_chat.send_message(
        "Выберите мастера",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return "order"


