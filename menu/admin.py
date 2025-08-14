from django.contrib import admin
from .models import MenuItem, Order


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 20


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'item_list')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'items__name')
    ordering = ('-created_at',)
    list_per_page = 20

    def item_list(self, obj):
        return ", ".join([item.name for item in obj.items.all()])
    item_list.short_description = "Sifariş elementləri"
