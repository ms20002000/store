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

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductSearchView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'brand', 'description']  


class ProductsByCategoryView(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            products = category.products.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
