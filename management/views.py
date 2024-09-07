import json

from _decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncMonth, Cast
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm, OrderStatusUpdateForm, OrderMaterialForm, MaterialOrderForm
from django.http import JsonResponse
from .models import Technician, Order, Material, OrderMaterial
from django.contrib.auth import authenticate, login
from .forms import TechnicianLoginForm
from .forms import TechnicianRegistrationForm
from .forms import TechnicianProfileForm
from django.db.models import Sum, Count, F, FloatField


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save()
            return redirect('order_status', order_id=new_order.id)
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})


def load_technicians(request):
    service_id = request.GET.get('service_id')
    technicians = Technician.objects.filter(service=service_id).order_by('name')
    return JsonResponse(list(technicians.values('id', 'name')), safe=False)


def order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_status.html', {'order': order})


from django.contrib import messages

def technician_login(request):
    if request.method == 'POST':
        form = TechnicianLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('technician_dashboard')  # Редирект на дашборд техника, замените на нужный URL
        else:
            messages.error(request, "Username or password is incorrect.")
    else:
        form = TechnicianLoginForm()
    return render(request, 'technician_login.html', {'form': form})



@login_required
def technician_profile(request):
    if request.method == 'POST':
        form = TechnicianProfileForm(request.POST, instance=request.user.technician)
        if form.is_valid():
            form.save()
            return redirect('technician_dashboard')
    else:
        form = TechnicianProfileForm(instance=request.user.technician)
    return render(request, 'technician_profile.html', {'form': form})


def register_technician(request):
    if request.method == 'POST':
        form = TechnicianRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Аутентификация пользователя
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)  # Вход пользователя в систему
                return redirect('new_order')  # Перенаправление на главную страницу или дашборд
    else:
        form = TechnicianRegistrationForm()
    return render(request, 'technician_register.html', {'form': form})

@login_required
def technician_dashboard(request):
    order_material_form = OrderMaterialForm()
    material_order_form = MaterialOrderForm()

    if request.method == 'POST':
        if 'add_material' in request.POST:
            order_material_form = OrderMaterialForm(request.POST)
            # Предыдущая логика сохранения
        elif 'order_material' in request.POST:
            material_order_form = MaterialOrderForm(request.POST)
            if material_order_form.is_valid():
                material_order_form.save()
                messages.success(request, 'Материал успешно заказан.')
    if request.method == 'POST' and 'add_material' in request.POST:
        order_material_form = OrderMaterialForm(request.POST)
        if order_material_form.is_valid():
            order_material = order_material_form.save(commit=False)
            order_material.order = Order.objects.get(pk=request.POST.get('order_id'))

            material_id = order_material_form.cleaned_data.get('material').id  # Assume material is a field in form

            try:
                material = Material.objects.get(id=material_id)
                if material.quantity >= order_material.quantity_used:
                    material.quantity -= order_material.quantity_used
                    material.save()
                    order_material.save()
                    messages.success(request, 'Материал успешно добавлен.')
                else:
                    messages.error(request, 'Не достаточно материала на складе.')
            except Material.DoesNotExist:
                messages.error(request, 'Материал с указанным ID не найден в базе данных.')

    technician_orders = Order.objects.filter(technician__user=request.user)
    completed_orders = Order.objects.filter(technician__user=request.user, status='completed')
    total_earnings = completed_orders.aggregate(total_income=Sum('service__price'), total_orders=Count('id'))

    context = {
        'orders': technician_orders,
        'order_material_form': order_material_form,
        'material_order_form': material_order_form,
        'total_earnings': total_earnings,
    }

    return render(request, 'technician_dashboard.html', context)

@login_required
def report_view(request):
    materials_data = get_materials_data()
    profits_data = get_profits_data()

    return render(request, 'report.html', {
        'materials_data': materials_data,
        'profits_data': profits_data,
    })


def get_materials_data():
    return list(OrderMaterial.objects
                .values('material__name')
                .annotate(total_quantity=Sum('quantity_used'))
                .order_by('material__name'))
def get_profits_data():
    # Вычисление стоимости материалов
    materials_profit = OrderMaterial.objects.aggregate(total_material_price=Sum(F('quantity_used') * F('material__price')))

    # Вычисление служебных сборов
    service_fees_profit = Technician.objects.aggregate(total_service_fee=Sum('service_fee'))

    # Подсчёт итоговой прибыли
    total_materials_profit = Decimal('0.20') * materials_profit['total_material_price'] if materials_profit['total_material_price'] else Decimal('0')
    total_service_fees_profit = Decimal('0.20') * service_fees_profit['total_service_fee'] if service_fees_profit['total_service_fee'] else Decimal('0')

    actual_profit = total_materials_profit + total_service_fees_profit

    # Возвращаем общую прибыль и детали прибыли
    return {
        'actual_profit': actual_profit,
        'materials_profit': total_materials_profit,
        'service_fees_profit': total_service_fees_profit
    }

def home(request):
    return render(request, 'home.html')



@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, technician__user=request.user)

    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('technician_dashboard')
    else:
        form = OrderStatusUpdateForm(instance=order)

    return render(request, 'edit_order.html', {'form': form, 'order': order})


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('technician_login')


