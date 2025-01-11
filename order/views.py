from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer
from .models import *
from discount.models import Coupon
from django.utils.timezone import now

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            cart = request.data.get("cart")
            total_price = request.data.get("total_price")
            discount_code = request.data.get("discount_code", "")

            # check discount code
            discount = self.validate_discount(discount_code)

            # Validate input data
            errors = self.validate_input_data(user, cart, total_price, discount)
            if errors:
                print(errors)
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            discount_code = discount.code if discount else discount_code
            order_data = self.set_order_data(user, cart, total_price, discount_code)
            serializer = OrderSerializer(data=order_data)
            if serializer.is_valid():
                order = serializer.save() 
                if discount_code: 
                    discount.mark_as_used()
                return Response(
                    {"order_id": order.id, "message": "Order created successfully."},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def validate_input_data(self, user, cart, total_price, discount_code):
        errors = {}
        # Validate user
        if not user or not Account.objects.filter(id=user.id).exists():
            errors['user'] = "Authenticated user does not exist."
        
        # Validate cart
        if not cart or len(cart) == 0:
            errors['cart'] = "Cart is empty."
        else:
            for item in cart:
                if not Product.objects.filter(id=item['id']).exists():
                    errors['cart'] = f"Product with ID {item['id']} does not exist."
                    break

        # Validate total_price
        calculated_total_price = sum(
            Product.objects.get(id=item['id']).price * item['quantity'] 
            for item in cart
        )
        if discount_code:
            calculated_total_price = round(float(calculated_total_price) * (1-0.3), 2)
        if float(total_price) != calculated_total_price:
            errors['total_price'] = "Total price does not match the sum of product prices."

        return errors
        
    def validate_discount(self, discount_code):
        try:
            discount = Coupon.objects.get(code=discount_code)
            if discount.expire_at < now() or discount.is_used:
                return ''
            return discount
        except Coupon.DoesNotExist:
            return ''
        
    def set_order_data(self, user, cart, total_price, discount_code):
        order_data = {
                "user": user.id, 
                "status": "completed",
                "total_price": total_price,
                "items": [
                    {
                        "product": item["id"],
                        "price": float(item["price"])
                    } for item in cart
                ],
                "coupon_code": discount_code
            }
        return order_data


class UserOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    

class CheckPurchasedProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        products = request.data.get('products', [])
        user = request.user

        purchased_products = OrderItem.objects.filter(
            order__user=user, 
            order__status='completed', 
            product__id__in=[product['id'] for product in products]
        ).values_list('product_id', flat=True)

        purchased_products_ids = set(purchased_products)
        remaining_products = [product for product in products if product['id'] not in purchased_products_ids]
        removed_products = [product for product in products if product['id'] in purchased_products_ids]

        return Response({
            'remainingProducts': remaining_products,
            'removedProducts': removed_products
        })