import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.ext import Updater, CommandHandler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def greet_user(update, context):
    update.message.reply_text('Приветствую')


class Command(BaseCommand):
    help = 'Телеграм Бот'

    def handle(self, *args, **options):
        updater = Updater(settings.TG_TOKEN, use_context=True)

        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', greet_user))

        logger.info('Бот запущен')
        updater.start_polling()
        updater.idle()
