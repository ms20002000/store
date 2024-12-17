from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedIdentityField(
        view_name='category-products',  
        lookup_field='name'              
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'category_photo', 'products']


# class CategorySerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True, read_only=True)

#     class Meta:
#         model = Category
#         fields = '__all__' 