from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
@csrf_exempt  
def create_order_api(request):
    if request.method == 'POST':
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
    
    return JsonResponse({'error': 'Yalnız POST sorğusu qəbul edilir.'}, status=405)

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