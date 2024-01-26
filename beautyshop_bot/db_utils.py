from beautyshop_bot.models import Salon, Order, Client


def get_salon_contacts():
    salons = Salon.objects.all()
    contacts = [
        {
            "name": salon.name,
            "address": salon.address,
            "phone": salon.phone,
        }
        for salon in salons
    ]
    return contacts


def get_client_orders(chat_id):
    client = Client.objects.get(telegram_chat_id=chat_id)
    orders = Order.objects.filter(customer=client)
    my_orders = [
        {
            'speciality': order.speciality,
            'master': order.master,
            'time': order.order_time
        }
        for order in orders
    ]
    return my_orders
