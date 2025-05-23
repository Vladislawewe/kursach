from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Reservation, MenuItem, Table, Employee, Order, OrderItem, Bill
from .forms import CustomerForm, ReservationForm, MenuItemForm, TableForm, EmployeeForm, OrderAssignEmployeeForm, OrderForm, OrderItemFormSet, BillForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime

def home(request):
    return render(request, 'booking/home.html')

@login_required
def customer_list(request):
    search_query = request.GET.get('search', '')
    customers = Customer.objects.all()
    if search_query:
        customers = customers.filter(name__icontains=search_query)
    return render(request, 'booking/customer_list.html', {'customers': customers, 'search_query': search_query})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'booking/customer_form.html', {'form': form})

@login_required
def reservation_list(request):
    status = request.GET.get('status')
    date = request.GET.get('date')
    reservations = Reservation.objects.all()
    if status:
        reservations = reservations.filter(status=status)
    if date:
        reservations = reservations.filter(date=date)
    return render(request, 'booking/reservation_list.html', {
        'reservations': reservations,
        'selected_status': status,
        'selected_date': date,
    })

def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            table = reservation.table
            table.status = 'busy'
            table.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'booking/reservation_form.html', {'form': form})

@login_required
def menu_list(request):
    items = MenuItem.objects.all()
    return render(request, 'booking/menu_list.html', {'items': items})

def menu_create(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'booking/menu_form.html', {'form': form})

def menu_update(request, pk):
    item = MenuItem.objects.get(pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'booking/menu_form.html', {'form': form})

def menu_delete(request, pk):
    item = MenuItem.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('menu_list')
    return render(request, 'booking/menu_confirm_delete.html', {'item': item})

@login_required
def table_list(request):
    status = request.GET.get('status')
    tables = Table.objects.all()
    if status:
        tables = tables.filter(status=status)
    return render(request, 'booking/table_list.html', {'tables': tables, 'selected_status': status})

def table_create(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Стол успешно добавлен!')
            return redirect('table_list')
    else:
        form = TableForm()
    return render(request, 'booking/table_form.html', {'form': form})

def table_update(request, pk):
    table = Table.objects.get(pk=pk)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('table_list')
    else:
        form = TableForm(instance=table)
    return render(request, 'booking/table_form.html', {'form': form})

def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == 'POST':
        table.delete()
        return redirect('table_list')
    return render(request, 'booking/table_confirm_delete.html', {'table': table})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'booking/employee_list.html', {'employees': employees})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'booking/employee_form.html', {'form': form})

def order_assign_employee(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        form = OrderAssignEmployeeForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderAssignEmployeeForm(instance=order)
    return render(request, 'booking/order_assign_employee.html', {'form': form, 'order': order})

@login_required
def order_list(request):
    table_id = request.GET.get('table')
    customer_id = request.GET.get('customer')
    orders = Order.objects.all()
    if table_id:
        orders = orders.filter(table_id=table_id)
    if customer_id:
        orders = orders.filter(customer_id=customer_id)
    tables = Table.objects.all()
    customers = Customer.objects.all()
    return render(request, 'booking/order_list.html', {
        'orders': orders,
        'tables': tables,
        'customers': customers,
        'selected_table': table_id,
        'selected_customer': customer_id
    })

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.instance = order
            formset.save()
            return redirect('order_list')
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, 'booking/order_form.html', {'form': form, 'formset': formset})

def order_update(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    return render(request, 'booking/order_form.html', {'form': form, 'formset': formset})

def order_delete(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'booking/order_confirm_delete.html', {'order': order})

def bill_list(request):
    bills = Bill.objects.all()
    return render(request, 'booking/bill_list.html', {'bills': bills})

def bill_create(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bill_list')
    else:
        form = BillForm()
    return render(request, 'booking/bill_form.html', {'form': form})

def bill_update(request, pk):
    bill = Bill.objects.get(pk=pk)
    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('bill_list')
    else:
        form = BillForm(instance=bill)
    return render(request, 'booking/bill_form.html', {'form': form})

def bill_delete(request, pk):
    bill = Bill.objects.get(pk=pk)
    if request.method == 'POST':
        bill.delete()
        return redirect('bill_list')
    return render(request, 'booking/bill_confirm_delete.html', {'bill': bill})

@login_required
def customer_update(request, pk):
    customer = Customer.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'booking/customer_form.html', {'form': form})

@login_required
def customer_delete(request, pk):
    customer = Customer.objects.get(pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'booking/customer_confirm_delete.html', {'customer': customer})

def reservation_update(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'booking/reservation_form.html', {'form': form})

def reservation_delete(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservation_list')
    return render(request, 'booking/reservation_confirm_delete.html', {'reservation': reservation})


def your_view(request):
    # ...
    messages.success(request, "Запись успешно добавлена!")
    messages.error(request, "Ошибка при добавлении записи.")
    # ...


def reports_view(request):
    date_str = request.GET.get('date')
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = timezone.now().date()

    # Оборот за день
    day_turnover = Bill.objects.filter(
        paid=True,
        issued_at__date=date
    ).aggregate(total=Sum('total'))['total'] or 0

    # Оборот за месяц
    month = date.month
    year = date.year
    month_turnover = Bill.objects.filter(
        paid=True,
        issued_at__year=year,
        issued_at__month=month
    ).aggregate(total=Sum('total'))['total'] or 0

    # Количество заказов за день
    orders_count = Bill.objects.filter(issued_at__date=date).count()

    # Самые популярные блюда
    popular_dishes = (
        OrderItem.objects
        .values('menu_item__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')[:5]
    )

    context = {
        'date': date,
        'day_turnover': day_turnover,
        'month_turnover': month_turnover,
        'orders_count': orders_count,
        'popular_dishes': popular_dishes,
    }
    return render(request, 'booking/reports.html', context)