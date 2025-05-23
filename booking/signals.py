from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation, Table, OrderItem, Bill

# Автоматическое обновление статуса столика при бронировании
@receiver(post_save, sender=Reservation)
def update_table_status_on_reservation(sender, instance, **kwargs):
    if instance.status == 'забронирован':
        instance.table.status = 'занят'
    else:
        instance.table.status = 'свободный'
    instance.table.save()

@receiver(post_delete, sender=Reservation)
def free_table_on_reservation_delete(sender, instance, **kwargs):
    if instance.table:
        instance.table.status = 'свободный'
        instance.table.save()

# Автоматический пересчет суммы счёта при изменении заказа
@receiver([post_save, post_delete], sender=OrderItem)
def update_bill_total(sender, instance, **kwargs):
    order = instance.order
    bill = Bill.objects.filter(order=order).first()
    if bill:
        total = sum(item.quantity * (item.price or 0) for item in order.orderitem_set.all())
        bill.total = total
        bill.save()