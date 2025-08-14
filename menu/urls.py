from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.menu_view, name='menu'),
    path('logout/', views.logout_view, name='logout'),
    path('orders/', views.orders_view, name='orders'),
    path('api/orders/', views.create_order_api, name='create_order_api'),
    path('orders/delete/<int:order_id>/', views.delete_order_view, name='delete_order'),
]
