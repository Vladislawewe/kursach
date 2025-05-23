from django.contrib import admin
from .models import Customer, Employee, Table, MenuItem, Reservation, Order, OrderItem, Bill

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Table)
admin.site.register(MenuItem)
admin.site.register(Reservation)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Bill)