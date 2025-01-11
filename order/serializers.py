from rest_framework import serializers
from .models import Order, OrderItem
from product.models import Product
from discount.models import Coupon

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'product_name']

    def get_product_name(self, obj):
        return obj.product.name


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    coupon_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = ['user', 'status', 'total_price', 'items', 'coupon_code', 'created_at']

    def validate(self, data):
        for item in data['items']:
            try:
                product = Product.objects.get(id=item['product'].id)
                if product.price != item['price']:
                    raise serializers.ValidationError(f"Invalid price for product {product.name}")
            except Product.DoesNotExist:
                raise serializers.ValidationError("Product does not exist.")

        if 'coupon_code' in data and data['coupon_code']:
            try:
                coupon = Coupon.objects.get(code=data['coupon_code'])
                data['coupon'] = coupon
            except Coupon.DoesNotExist:
                raise serializers.ValidationError("Invalid coupon code.")

        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        coupon = validated_data.pop('coupon', None)
        validated_data.pop('coupon_code', None) 
        order = Order.objects.create(coupon=coupon, **validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
