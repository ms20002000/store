import csv
from django.http import HttpResponse
from django.utils.timezone import now
from django.core.mail import send_mail
from django.contrib import admin
from django.db.models import QuerySet
from .models import *

@admin.action(description="Activate discount for selected products")
def activate_discount(modeladmin, request, queryset: QuerySet):
    queryset.update(discount=True)


@admin.action(description="Download as CSV")
def export_as_csv(modeladmin, request, queryset):
    model = queryset.model  
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model._meta.model_name}_data.csv"'

    writer = csv.writer(response)
    headers = [field.verbose_name for field in model._meta.fields]
    writer.writerow(headers)

    for obj in queryset:
        row = [getattr(obj, field.name) for field in model._meta.fields]
        writer.writerow(row)

    return response


@admin.action(description="Deactivate expired products")
def deactivate_expired_products(modeladmin, request, queryset):
    expired_products = queryset.filter(expire_at__lt=now())
    count = expired_products.update(is_active=False)  
    modeladmin.message_user(request, f"{count} Deactivated") 


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'category_photo')
    search_fields = ('name',)
    list_filter = ('parent',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'price', 'category', 'discount', 'course_time', 'prerequisite')
    search_fields = ('name', 'teacher', 'category__name')
    list_filter = ('category', 'discount')
    ordering = ('name',)
    list_per_page = 20
    fields = ('name', 'teacher', 'price', 'description', 'category', 'discount', 'course_time', 'prerequisite')
    actions = [activate_discount, export_as_csv, deactivate_expired_products]


@admin.register(ProductFile)
class ProductFileAdmin(admin.ModelAdmin):
    list_display = ('product', 'product_photo')
    search_fields = ('product__name',)
    list_filter = ('product',)
    ordering = ('product',)


@admin.register(TopicFile)
class TopicFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'description', 'topic_photo')
    search_fields = ('title', 'product__name')
    list_filter = ('product',)
    ordering = ('title',)


@admin.register(TopicMedia)
class TopicMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic_file', 'description', 'topic_movie')
    search_fields = ('title', 'topic_file__product__name')
    list_filter = ('topic_file__product',)
    ordering = ('title',)


@admin.register(Attributes)
class AttributesAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ('name', 'value')
    list_filter = ('name',)
    ordering = ('name',)
