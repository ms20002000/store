from django.contrib import admin
from .models import *


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
