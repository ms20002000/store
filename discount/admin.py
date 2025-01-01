from django.contrib import admin
from discount.models import Discount, Coupon

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount', 'start_date', 'expire_at', 'max_amount', 'created_at')
    list_filter = ('expire_at', 'created_at')
    search_fields = ('discount',)
    ordering = ('-expire_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('amount', 'start_date', 'expire_at', 'max_amount', 'created_at', 'min_price')
    list_filter = ('expire_at', 'created_at')
    search_fields = ('amount',)
    ordering = ('-expire_at',)
    readonly_fields = ('created_at',)
