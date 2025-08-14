from django.urls import path
from . import views



urlpatterns = [

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.menu_view, name='menu'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/delete/<int:order_id>/', views.delete_order_view, name='delete_order'),
    path('menu/update/<int:item_id>/api/', views.update_menu_item_api, name='update_menu_item_api'),
    path('api/orders/', views.create_order_api, name='create_order_api'),
    path('orders/update/<int:order_id>/api/', views.update_order_api, name='update_order_api'),
]
