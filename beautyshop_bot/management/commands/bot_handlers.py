from .bot_utils import main_keyboard


def greet_user(update, context):
    chat_id = update.effective_chat.id
    with open('static/greting_salon.jpg', 'rb') as photo_file:
        context.bot.send_photo(chat_id=chat_id, photo=photo_file)

    welcome_message = 'Приветствуем в нашем боте. 🌹🌹🌹 Поможем выбрать услугу, записаться к мастеру в удобное для вас время.'
    update.message.reply_text(welcome_message, reply_markup=main_keyboard())
