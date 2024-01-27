from datetime import datetime, timedelta

from beautyshop_bot.models import Salon, Master, Speciality, Order, Client
import zoneinfo


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


def get_masters():
    masters = Master.objects.all()
    result = [
        {
            "name": master.name,
            "surname": master.surname,
            "specialities": [
                sp.name for sp in master.speciality.all()
            ]
        }
        for master in masters
    ]
    return result

  
def get_master_and_timeslots(master_name, date_time=None):
    master = Master.objects.filter(name=master_name).first()
    if date_time:
        orders_for_master = Order.objects.filter(
            master=master,
            order_time=date_time,
        )
    else:
        orders_for_master = Order.objects.filter(
            master=master,
        )
    today_date = datetime.today().\
        replace(tzinfo=zoneinfo.ZoneInfo("Europe/Moscow"))

    occupied_hours = [ ts.order_time for ts in orders_for_master]

    available_time_slots = master.working_hours.filter(start_time__gt=today_date).all()
    hours = {}
    for ts in available_time_slots:
        hours[ts.salon.name] = hours.get(ts.salon.name, [])
        hours[ts.salon.name].extend(list(
            ts.start_time + timedelta(hours=i) for i in range(0, (ts.end_time.hour - ts.start_time.hour)) if ts.start_time + timedelta(hours=i) not in occupied_hours
        ))
    return hours


def get_free_masters(date_time):
    masters = get_masters()
    necessary_date = datetime.strptime(date_time, "%d/%m - %H")
    necessary_date = necessary_date.\
        replace(year=datetime.now().year).\
        replace(tzinfo=zoneinfo.ZoneInfo("Europe/Moscow"))

    available_masters = []
    for master in masters:
        time_slots = get_master_and_timeslots(master["name"])
        for salon, slots in time_slots.items():
            if necessary_date in slots:
                available_masters.append(
                    {
                        "name": master["name"],
                        "surname": master["surname"],
                        "specialities": master["specialities"],
                        "salon": salon,
                    }
                )
    return available_masters



  
def make_order(order_data):
    client = Client.objects.get_or_create(
        name=order_data['client_name'],
        surname=order_data['client_surname'],
        phone=order_data["phone"],
        telegram_chat_id=order_data["telegram_chat_id"],
        telegram_nickname=order_data["telegram_nickname"],
    )
    # print(client)
    master = Master.objects.filter(name=order_data['master_name']).first()
    # print(master)
    order = Order.objects.get_or_create(
        customer=client[0],
        master=master,
        order_time=datetime.strptime(order_data['date'], "%d/%m - %H").
            replace(year=datetime.now().year).
            replace(tzinfo=zoneinfo.ZoneInfo("Europe/Moscow")),
    )
    # print(order)
    return order

def check_if_user_exists(chat_id):
    client = Client.objects.filter(telegram_chat_id=chat_id).first()
    if client:
        return {
            "client_name": client.name,
            "client_surname": client.surname,
            "phone": client.phone,
            "telegram_chat_id": client.telegram_chat_id,
            "telegram_nickname": client.telegram_nickname,
        }
    return False

  
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


def get_dates():
    cur_date = datetime.now()
    return [
        cur_date + timedelta(days=i) for i in range(30)
    ]
