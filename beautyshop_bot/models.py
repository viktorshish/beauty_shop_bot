from django.db import models


class Salon(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название салона",
    )
    address = models.CharField(
        max_length=200,
        verbose_name="Адрес салона",
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон салона",
    )

    def __str__(self):
        return f"{self.name} - {self.address} - {self.phone}"

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'


class TimeSlot(models.Model):
    start_time = models.DateTimeField(
        verbose_name="Начало смены",
    )
    end_time = models.DateTimeField(
        verbose_name="Конец смены",
    )
    salon = models.ForeignKey(
        Salon,
        verbose_name="Салон смены",
        related_name="shifts",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.start_time.day}:{self.start_time.month} - {self.start_time.hour} - {self.end_time.hour}, {self.salon.address}"

    class Meta:
        verbose_name = 'Смены'
        verbose_name_plural = 'Смены'


class Speciality(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название услуги",
    )
    description = models.TextField(
        verbose_name="Описание услуги",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуги'
        verbose_name_plural = 'Услуги'
        ordering = ['-name']


class Master(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя",
    )
    surname = models.CharField(
        max_length=100,
        verbose_name="Фамилия",
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон",
    )
    telegram = models.CharField(
        max_length=30,
        verbose_name="Телеграмм",
    )
    working_hours = models.ManyToManyField(
        TimeSlot,
        verbose_name="Смены",
        related_name="master",
    )
    speciality = models.ManyToManyField(
        Speciality,
        verbose_name="Услуги",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class Client(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя",
    )
    surname = models.CharField(
        max_length=100,
        verbose_name="Фамилия",
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон",
    )
    telegram_chat_id = models.CharField(
        max_length=30,
        verbose_name="Телеграмм",
    )
    telegram_nickname = models.CharField(
        max_length=30,
        verbose_name="Ник в телеграме",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Order(models.Model):
    customer = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Клиент",
        related_name="orders",
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name="Мастер",
        related_name="orders",
    )
    order_time = models.DateTimeField(
        verbose_name="Начало записи",
    )
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.CASCADE,
        verbose_name="Тип услуги",
        null=True,
    )

    def __str__(self):
        return f"{self.customer.name} - {self.master.name} - {self.order_time.hour} - {self.speciality}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
