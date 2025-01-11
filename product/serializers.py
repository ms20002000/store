from rest_framework import serializers
from .models import Product, Category, ProductFile, TopicFile, TopicMedia
from order.models import Order

class ProductFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFile
        fields = ['id', 'product_movie', 'product_photo']

class TopicMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicMedia
        fields = ['id', 'title', 'description', 'topic_movie']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        product = self.context.get('product')

        if request and request.user.is_authenticated:
            if Order.objects.filter(user=request.user, items__product=product, status='completed').exists():
                return representation
        return {}


class ProductTopicFileSerializer(serializers.ModelSerializer):
    topic_media = TopicMediaSerializer(many=True, read_only=True)
    class Meta:
        model = TopicFile
        fields = ['id', 'title', 'description', 'topic_photo', 'topic_media']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        product = self.context.get('product')
        self.fields['topic_media'].context.update({
            'request': request,
            'product': product
        })
        return representation


class ProductSerializer(serializers.ModelSerializer):
    product_file = ProductFileSerializer(many=True, read_only=True)
    product_topic_file = ProductTopicFileSerializer(many=True, read_only=True, source='topic_file')
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        self.fields['product_topic_file'].context.update({
            'request': request,
            'product': instance
        })
        return representation


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedIdentityField(
        view_name='category-products',  
        lookup_field='name'              
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'category_photo', 'products', 'parent']


class SubCategorySerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedIdentityField(
        view_name='category-products',  
        lookup_field='name'              
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'products']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AllCategorySerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedIdentityField(
        view_name='category-products',  
        lookup_field='name'              
    )
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories', 'products']