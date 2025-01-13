from rest_framework.permissions import IsAuthenticated
from order.models import Order, OrderItem
from product.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .redis import OTPCode
from .serializers import UserRegistrationSerializer, EditProfileSerializer, LoginSerializer
from .utils import send_otp_email
from rest_framework_simplejwt.tokens import RefreshToken
from product.serializers import ProductSerializer
from django.shortcuts import get_object_or_404


class RegisterView(APIView):
    def get(self, request):
        serializer = UserRegistrationSerializer()
        return Response({
            "fields": serializer.data,
            "instructions": "Fill in the above fields and send a POST request to this endpoint."
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            email = validated_data.get('email')

            otp_code = OTPCode.generate_code()
            OTPCode.save_otp_to_redis(email, otp_code)
            send_otp_email.delay(email, otp_code)
            OTPCode.save_user_data_to_redis(email, serializer.data)

            return Response({
                "message": "Registration details are valid. An OTP has been sent to your email."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
        login = request.data.get('is_login_code')

        if not email or not otp_code:
            return Response({"error": "Email and OTP code are required."}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = OTPCode.get_otp_code(email)        
        if stored_otp and stored_otp.decode() == otp_code:
            if login == 'true':
                user = CustomUser.objects.get(email=email)
                return set_token(user, email)
            
            if (user_data:=OTPCode.get_user_data(email)):
                user_serializer = UserRegistrationSerializer(data=user_data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    return set_token(user, email, login=False)
                print(user_serializer.errors)
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "User data not found. Please restart registration."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            otp_code = OTPCode.generate_code()
            OTPCode.save_otp_to_redis(email, otp_code)
            send_otp_email.delay(email, otp_code)
            return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found. Please register first."}, status=status.HTTP_404_NOT_FOUND)
        


class UserPurchasedProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        completed_orders = Order.objects.filter(user=request.user, status='completed')
        purchased_products = Product.objects.filter(
            id__in=OrderItem.objects.filter(order__in=completed_orders).values_list('product_id', flat=True)
        ).distinct()

        products_data = ProductSerializer(purchased_products, many=True).data
        return Response({"products": products_data})


class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = EditProfileSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = EditProfileSerializer(instance=user, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully!",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginPasswordView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(CustomUser, email=email)
            return set_token(user, email)
        else:
            return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)


def set_token(user, email, login=True):
    refresh = RefreshToken.for_user(user)
    if login:
        status_code = status.HTTP_200_OK
    else:
        status_code = status.HTTP_201_CREATED
    response = Response({
        "message": "Login successful.",
        "refresh": str(refresh),  
        "email": email,
        "profile_picture": user.profile_picture,
    }, status=status_code)
    
    # set access token in cookie
    response.set_cookie(
        key='access_token',
        value=str(refresh.access_token),
        httponly=False, 
        samesite='Lax',  
    )
    return response
