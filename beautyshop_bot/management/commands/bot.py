import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardMarkup


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def greet_user(update, context):
    chat_id = update.effective_chat.id
    with open('static/greting_salon.jpg', 'rb') as photo_file:
        context.bot.send_photo(chat_id=chat_id, photo=photo_file)

    start_keyboard = ReplyKeyboardMarkup([
        ['Запись', 'Мои записи'],
        ['Контакты салонов', 'Запись по телефону']
    ])
    update.message.reply_text('Приветствую', reply_markup=start_keyboard)


class Command(BaseCommand):
    help = 'Телеграм Бот'

    def handle(self, *args, **options):
        updater = Updater(settings.TG_TOKEN, use_context=True)

        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', greet_user))

        logger.info('Бот запущен')
        updater.start_polling()
        updater.idle()
