from beautyshop_bot.models import Salon, Master


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
            "surname": master.name,
            "specialities": [
                sp.name for sp in master.speciality
            ]
        }
        for master in masters
    ]
    return result