from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.filters import SearchFilter


class CustomPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_name = self.kwargs['name']  
        return Product.objects.filter(category__name=category_name)
    

class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        limit = self.request.query_params.get('limit')
        if limit:
            queryset = queryset[:int(limit)]
        return queryset
    
class CategoryDetailView(RetrieveAPIView):
    serializer_class = CategorySerializer

    def get_object(self):
        category_name = self.kwargs['name']
        category = get_object_or_404(
            Category.objects.filter(name=category_name)   
        )
        return category
    
class SubcategoryListView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        parent_name = self.kwargs.get('parent_name')  
        parent = get_object_or_404(Category, name=parent_name)  
        return Category.objects.filter(parent=parent)

    
class ProductListView(ListAPIView):
    queryset = Product.objects.prefetch_related('product_file').all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        limit = self.request.query_params.get('limit')
        if limit:
            queryset = queryset[:int(limit)]
        return queryset


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        product_name = self.kwargs['name']
        product = get_object_or_404(
            Product.objects.prefetch_related('product_file', 'topic_file'), 
            name=product_name
        )
        return product


class ProductSearchView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'teacher', 'description']  
    

