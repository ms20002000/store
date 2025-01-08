from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),
    path('products/<str:name>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category/products/<str:name>/', CategoryProductsView.as_view(), name='category-products'),
    path('categories/<str:parent_name>/subcategories/', SubcategoryListView.as_view(), name='subcategory-list'),
    path('allcategories/', AllCategoryListView.as_view(), name='allcategory-list'),
]


