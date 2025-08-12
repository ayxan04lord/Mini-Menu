from django.urls import path
from .views import RegisterView, LoginView, MenuListView, OrderListCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('menu/', MenuListView.as_view(), name='menu-list'),
    path('orders/', OrderListCreateView.as_view(), name='orders'),
]