from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
import json

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart_data = request.COOKIES.get('cart')
            if not cart_data:
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            cart = json.loads(cart_data)

            order_data = {
                "user": request.user.id,
                "status": "pending",
                "payment_method": request.data.get("payment_method"),
                "total_price": sum(item['price'] * item['quantity'] for item in cart),
                "items": [
                    {
                        "product": item['id'],
                        "price": item['price']
                    } for item in cart
                ],
                "coupon_code": request.data.get("coupon_code", "")
            }

            serializer = OrderSerializer(data=order_data)
            if serializer.is_valid():
                order = serializer.save()
                return Response({"order_id": order.id, "message": "Order created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
