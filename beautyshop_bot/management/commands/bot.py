import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from .bot_handlers import greet_user, show_contacts
from .bot_booking import booking_start


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Телеграм Бот'

    def handle(self, *args, **options):
        updater = Updater(settings.TG_TOKEN, use_context=True)

        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', greet_user))

        dp.add_handler(MessageHandler(Filters.regex('^(Контакты)$'), show_contacts))
        booking = ConversationHandler(
            entry_points=[
                MessageHandler(Filters.regex('^(Хочу записаться)$'), booking_start)
            ],
            states={},
            fallbacks=[]
        )
        dp.add_handler(booking)

        logger.info('Бот запущен')
        updater.start_polling()
        updater.idle()
