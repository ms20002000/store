from django.contrib import admin
from discount.models import Discount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount', 'expire_at', 'max_amount', 'created_at', 'updated_at')
    list_filter = ('expire_at', 'created_at')
    search_fields = ('discount',)
    ordering = ('-expire_at',)
    readonly_fields = ('created_at', 'updated_at')
