from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),
    path('category/products/<str:name>/', CategoryProductsView.as_view(), name='category-products'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]
