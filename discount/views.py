from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from discount.models import Coupon
from rest_framework.permissions import IsAuthenticated


class UseCouponView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        code = request.data.get("code")
        user = request.user

        try:
            # Find the coupon
            coupon = Coupon.objects.get(code=code, user=user)

            # Check if the coupon is expired or already used
            if coupon.expire_at < now():
                return Response({"error": "Coupon has expired."}, status=status.HTTP_400_BAD_REQUEST)
            if coupon.is_used:
                return Response({"error": "Coupon has already been used."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"success": "Coupon applied successfully.", "discount": coupon.amount}, status=status.HTTP_200_OK)
        except Coupon.DoesNotExist:
            return Response({"error": "Invalid coupon or not authorized."}, status=status.HTTP_404_NOT_FOUND)
