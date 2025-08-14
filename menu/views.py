from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import RegisterForm
from .models import MenuItem, Order


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('menu')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'İstifadəçi {username} uğurla qeydiyyatdan keçdi!')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def menu_view(request):
    items = MenuItem.objects.all()

    if request.method == 'POST':
        selected_item_ids = request.POST.getlist('items')
        if selected_item_ids:
            order = Order.objects.create(user=request.user)
            order.items.set(MenuItem.objects.filter(id__in=selected_item_ids))
            messages.success(request, "Sifarişiniz uğurla yaradıldı!")
            return redirect('orders')
        else:
            messages.error(request, "Ən azı bir məhsul seçməlisiniz.")

    return render(request, 'menu.html', {'menu_items': items})


@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@csrf_exempt
def update_menu_item_api(request, item_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Yalnız POST sorğusu qəbul edilir.'}, status=405)

    try:
        data = json.loads(request.body)
        name = data.get('name')
        price = data.get('price')

        if not name or price is None:
            return JsonResponse({'error': 'Ad və qiymət boş ola bilməz.'}, status=400)

        item = get_object_or_404(MenuItem, id=item_id)
        item.name = name
        item.price = price
        item.save()

        return JsonResponse({'message': f'{item.name} uğurla yeniləndi!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@csrf_exempt
def create_order_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Yalnız POST sorğusu qəbul edilir.'}, status=405)

    try:
        data = json.loads(request.body)
        item_ids = data.get('items', [])

        if not item_ids:
            return JsonResponse({'error': 'Ən azı bir məhsul seçməlisiniz.'}, status=400)

        order = Order.objects.create(user=request.user)
        order.items.set(MenuItem.objects.filter(id__in=item_ids))
        return JsonResponse({'message': 'Sifariş uğurla yaradıldı!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def delete_order_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Sifariş tapılmadı.'}, status=404)

    if request.method == 'POST':
        order.delete()
        return JsonResponse({'message': 'Sifariş uğurla silindi.'})

    return HttpResponseForbidden()


@login_required
def update_order_api(request, order_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Yalnız POST sorğusu qəbul edilir.'}, status=405)

    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Sifariş tapılmadı.'}, status=404)

    try:
        data = json.loads(request.body)
        item_ids = data.get('items', [])
        order.items.set(MenuItem.objects.filter(id__in=item_ids))
        order.save()

        items_data = [{'id': i.id, 'name': i.name, 'price': i.price} for i in order.items.all()]
        return JsonResponse({'message': 'Sifariş uğurla yeniləndi!', 'items': items_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
