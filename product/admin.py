from django.contrib import admin
from product.models import Category, Product, Attributes

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'stock_quantity', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'brand', 'created_at')
    search_fields = ('name', 'brand', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Attributes)
class AttributesAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'created_at', 'updated_at')
    search_fields = ('name', 'value')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
