from django.contrib import admin
from order.models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_method', 'address', 'created_at', 'updated_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__phone_number', 'address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'order__id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
