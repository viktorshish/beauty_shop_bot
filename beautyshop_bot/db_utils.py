from beautyshop_bot.models import Salon, Master, Speciality, Order

from datetime import datetime, timedelta


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

# def get_avalible_timeslots(master):
#
#     orders_for_master = Order.objects.filter(
#         master=master,
#     )
#     occupied_hours = [ ts.order_time.hour for ts in orders_for_master]
#     print(occupied_hours)
#     availible_time_slots = master.working_hours.all()
#
#     # avaible_hours = [[(slot.start_time.hour, slot.end_time.hour, slot.salon.address) for slot in ]  for ts in availible_time_slots if ts.start_time.hour not in occupied_hours]
#
#     # dt1 = YourModel.objects.get(pk=1).datetime_field1
#     # dt2 = YourModel.objects.get(pk=1).datetime_field2
#
#     # Calculate the time difference
#     # time_difference = dt2 - dt1
#
#     # Generate a list of all hours between the two DateTimeField values
#     avaible_hours = [
#         [
#             (
#                 ts.start_time.hour + i, ts.start_time.hour + i + 1, ts.salon.name
#             ) for i in range(0, (ts.end_time.hour - ts.start_time.hour)) if ts.start_time.hour + i not in occupied_hours
#         ]
#         for ts in availible_time_slots
#     ]
#
#     print(avaible_hours)
#
#     return avaible_hours



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

def get_master_and_timeslots(master_name):
    master = Master.objects.filter(name=master_name).first()
    # print(master)
    orders_for_master = Order.objects.filter(
        master=master,
    )
    # print(orders_for_master)
    occupied_hours = [ ts.order_time for ts in orders_for_master]

    # print(occupied_hours)
    available_time_slots = master.working_hours.all()
    # print(available_time_slots)
    available_hours = [
        [
            (
                ts.start_time + timedelta(hours=i), ts.start_time + timedelta(hours=i + 1), ts.salon.name
            ) for i in range(0, (ts.end_time.hour - ts.start_time.hour)) if ts.start_time + timedelta(hours=i) not in occupied_hours
        ]
        for ts in available_time_slots
    ]

    available_hours_dict = {}

    return available_hours


