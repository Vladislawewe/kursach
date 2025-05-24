from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation, Table, OrderItem, Bill
from .constants import (
    STATUS_FREE, STATUS_OCCUPIED, STATUS_RESERVED,
    RESERVATION_STATUS_CONFIRMED, RESERVATION_STATUS_CANCELLED
)


@receiver(post_save, sender=Reservation)
def update_table_status_on_reservation(sender, instance, **kwargs):
    # Согласуем статусы: если подтверждено — столик занят, если отменено — освобождаем
    if instance.table:
        if instance.status == RESERVATION_STATUS_CONFIRMED:
            instance.table.status = STATUS_OCCUPIED
        elif instance.status == RESERVATION_STATUS_CANCELLED:
            instance.table.status = STATUS_FREE
        instance.table.save()

@receiver(post_delete, sender=Reservation)
def free_table_on_reservation_delete(sender, instance, **kwargs):
    # Если бронирование удалено, освобождаем столик
    if instance.table:
        instance.table.status = STATUS_FREE
        instance.table.save()


@receiver([post_save, post_delete], sender=OrderItem)
def update_bill_total(sender, instance, **kwargs):
    order = instance.order
    bill = Bill.objects.filter(order=order).first()
    if bill:
        # Цена берется теперь через menu_item.price
        total = sum(item.quantity * (item.menu_item.price if item.menu_item else 0) for item in order.orderitem_set.all())
        bill.total = total
        bill.save(update_fields=['total'])