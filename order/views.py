from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer
from .models import Order
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

            if not cart or len(cart) == 0:
                return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            # check discount code
            if Coupon.objects.filter(code=discount_code).exists():
                discount = Coupon.objects.get(code=discount_code)
                if discount.expire_at < now() or discount.is_used:
                    discount_code = ''
                else:
                    discount.mark_as_used()
            else:
                discount_code = ''
                    

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

            serializer = OrderSerializer(data=order_data)
            if serializer.is_valid():
                order = serializer.save()  
                return Response(
                    {"order_id": order.id, "message": "Order created successfully."},
                    status=status.HTTP_201_CREATED
                )

            print(discount_code)
            print(total_price)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)