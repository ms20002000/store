from rest_framework import serializers
from .models import Product, Category, ProductFile, TopicFile

class ProductFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFile
        fields = ['id', 'product_movie', 'product_photo']

class ProductTopicFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicFile
        fields = ['id', 'name', 'description', 'product_movie', 'product_photo']


class ProductSerializer(serializers.ModelSerializer):
    product_file = ProductFileSerializer(many=True, read_only=True)
    product_topic_file = ProductTopicFileSerializer(many=True, read_only=True, source='topic_file')
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
        fields = ['id', 'name', 'category_photo', 'products', 'parent']

