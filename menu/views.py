from pyexpat.errors import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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

@login_required
def menu_view(request):
    items = MenuItem.objects.all()
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if item_id:
            item = MenuItem.objects.get(id=item_id)
            Order.objects.create(user=request.user, item=item)

    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'menu/menu.html', {'menu_items': items, 'user_orders': user_orders})

def logout_view(request):
    logout(request)

    return redirect("login")

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


def menu_view(request):
   items = MenuItem.objects.all()
   return render(request, 'menu.html', {'menu_items': items})
