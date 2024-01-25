from django.contrib import admin
from beautyshop_bot.models import Salon, TimeSlot, Speciality, Master, Client, Order

# Register your models here.

admin.site.register(Salon)
admin.site.register(TimeSlot)
admin.site.register(Master)
admin.site.register(Order)
admin.site.register(Speciality)
admin.site.register(Client)