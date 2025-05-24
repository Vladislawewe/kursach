from django.db import models
from django.core.validators import RegexValidator
from .constants import (
    TABLE_STATUS_CHOICES, STATUS_FREE, STATUS_RESERVED,
    RESERVATION_STATUS_CHOICES, RESERVATION_STATUS_PENDING
)

class Customer(models.Model):
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField(
        'Телефон', max_length=16, unique=True,
        validators=[RegexValidator(r'^\+7\d{10}$', message="Формат: +79991234567")]
    )
    email = models.EmailField('Электронная почта', null=True, blank=True)
    registered_at = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField('Имя', max_length=100)
    role = models.CharField('Должность', max_length=50)
    phone = models.CharField('Телефон', max_length=30, null=True, blank=True)
    email = models.EmailField('Электронная почта', null=True, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f"{self.name} ({self.role})"

class Table(models.Model):
    number = models.IntegerField('Номер столика', unique=True)
    seats = models.IntegerField('Количество мест')
    status = models.CharField('Статус', max_length=20, choices=TABLE_STATUS_CHOICES, default=STATUS_FREE)

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'

    def __str__(self):
        return f"Столик {self.number} ({self.seats} мест)"

class MenuItem(models.Model):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)
    available = models.BooleanField('Доступно', default=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, verbose_name='Столик')
    reserved_at = models.DateTimeField('Дата и время бронирования')
    guests = models.IntegerField('Количество гостей')
    status = models.CharField('Статус', max_length=20, choices=RESERVATION_STATUS_CHOICES, default=RESERVATION_STATUS_PENDING)
    comment = models.TextField('Комментарий', null=True, blank=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f"Бронь столика {self.table} для {self.customer}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Клиент')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, verbose_name='Столик')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name='Сотрудник')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Бронирование')
    created_at = models.DateTimeField('Дата заказа', auto_now_add=True)
    status = models.CharField('Статус', max_length=30, default='open')
    items = models.ManyToManyField(MenuItem, through='OrderItem', related_name='order_items', verbose_name='Блюда')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, verbose_name='Блюдо')
    quantity = models.IntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def save(self, *args, **kwargs):
        if not self.price and self.menu_item:
            self.price = self.menu_item.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.menu_item} x {self.quantity}"

class Bill(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    issued_at = models.DateTimeField('Дата выставления', auto_now_add=True)
    total = models.DecimalField('Сумма', max_digits=10, decimal_places=2, default=0, editable=False)
    paid = models.BooleanField('Оплачен', default=False)
    payment_method = models.CharField('Способ оплаты', max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = 'Счёт'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f"Счёт {self.id} ({'оплачен' if self.paid else 'не оплачен'})"