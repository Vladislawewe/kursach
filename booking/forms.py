from django import forms
from .models import Customer, Reservation, MenuItem, Table, Employee, Order, OrderItem, Bill
from .constants import RESERVATION_STATUS_CHOICES, TABLE_STATUS_CHOICES

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']
        labels = {
            'name': 'Имя',
            'phone': 'Телефон',
            'email': 'Электронная почта'
        }

class ReservationForm(forms.ModelForm):
    status = forms.ChoiceField(choices=RESERVATION_STATUS_CHOICES, label='Статус')
    class Meta:
        model = Reservation
        fields = ['customer', 'table', 'reserved_at', 'guests', 'status', 'comment']
        labels = {
            'customer': 'Клиент',
            'table': 'Столик',
            'reserved_at': 'Дата и время',
            'guests': 'Количество гостей',
            'status': 'Статус',
            'comment': 'Комментарий'
        }
        widgets = {
            'reserved_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'available']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'available': 'Доступно'
        }

class TableForm(forms.ModelForm):
    status = forms.ChoiceField(choices=TABLE_STATUS_CHOICES, label='Статус')
    class Meta:
        model = Table
        fields = ['number', 'seats', 'status']
        labels = {
            'number': 'Номер столика',
            'seats': 'Количество мест',
            'status': 'Статус'
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'role', 'phone', 'email']
        labels = {
            'name': 'Имя',
            'role': 'Должность',
            'phone': 'Телефон',
            'email': 'Электронная почта'
        }

class OrderAssignEmployeeForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['employee']
        labels = {'employee': 'Сотрудник'}

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'table', 'employee', 'reservation', 'status']
        labels = {
            'customer': 'Клиент',
            'table': 'Столик',
            'employee': 'Сотрудник',
            'reservation': 'Бронирование',
            'status': 'Статус'
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity', 'price']
        labels = {
            'menu_item': 'Блюдо',
            'quantity': 'Количество',
            'price': 'Цена'
        }

OrderItemFormSet = forms.inlineformset_factory(
    Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True
)

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['order', 'paid', 'payment_method']
        labels = {
            'order': 'Заказ',
            'paid': 'Оплачен',
            'payment_method': 'Способ оплаты'
        }