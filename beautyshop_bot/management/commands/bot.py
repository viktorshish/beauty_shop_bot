import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from .bot_booking import (booking_start, booking_surname, booking_method_choice,
                          booking_method_1, booking_method_2, booking_method_3,
                          booking_master, create_order, booking_date, booking_time, booking_phone, booking_method_4)
from .bot_handlers import (greet_user, show_contacts, show_my_orders, show_speciality, welcome_pdf_user,
                           not_accept_personal_data)
from .bot_utils import personal_data_keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Телеграм Бот'

    def handle(self, *args, **options):
        updater = Updater(settings.TG_TOKEN, use_context=True)

        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', welcome_pdf_user))

        dp.add_handler(MessageHandler(Filters.regex('^(Принимаю)$'), greet_user))

        dp.add_handler(MessageHandler(Filters.regex('^(Не принимаю)$'), not_accept_personal_data))

        dp.add_handler(MessageHandler(Filters.regex('^(Контакты)$'), show_contacts))
        
        booking = ConversationHandler(
            entry_points=[
                MessageHandler(Filters.regex('^(Хочу записаться)$'), booking_start)
            ],
            states={
                # "start": [MessageHandler(Filters.text, greet_user)],
                "name": [MessageHandler(Filters.text, booking_surname)],
                "surname": [MessageHandler(Filters.text, booking_phone)],
                "phone": [MessageHandler(Filters.text, booking_method_choice)],
                "method_choice": [MessageHandler(Filters.text, booking_method_choice)],
                "booking": [
                    MessageHandler(Filters.regex('В салон'), booking_method_1),
                    MessageHandler(Filters.regex('К мастеру'), booking_method_2),
                    MessageHandler(Filters.regex('На время'), booking_method_3),
                    MessageHandler(Filters.regex('По номеру телефона'), booking_method_4),
                ],
                "booking_master": [MessageHandler(Filters.text, booking_master)],

                "booking_date": [CallbackQueryHandler(booking_date, pattern="^(date|)")],
                "booking_time": [CallbackQueryHandler(booking_time, pattern="^(time|)")],


                "order": [MessageHandler(Filters.text, create_order)],
            },
            fallbacks=[]
        )
        dp.add_handler(booking)

        dp.add_handler(MessageHandler(Filters.regex('^(Мои записи)$'), show_my_orders))

        dp.add_handler(MessageHandler(Filters.regex('^(Услуги)$'), show_speciality))

        logger.info('Бот запущен')
        updater.start_polling()
        updater.idle()
