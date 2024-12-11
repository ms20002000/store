from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group
from .models import CustomUser, OTPCode
from .serializers import UserRegistrationSerializer
from .utils import send_otp_email
from rest_framework_simplejwt.tokens import RefreshToken

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
            print(validated_data)
            email = validated_data.get('email')

            otp_code = OTPCode.generate_code()
            OTPCode.save_otp_to_redis(email, otp_code)
            send_otp_email(email, otp_code)
            OTPCode.save_user_data_to_redis(email, serializer.data)

            return Response({
                "message": "Registration details are valid. An OTP has been sent to your email."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyRegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')

        if not email or not otp_code:
            return Response({"error": "Email and OTP code are required."}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = OTPCode.get_otp('otp', email)
        if stored_otp and stored_otp.decode() == otp_code:
            user_data = OTPCode.get_otp('user_data', email)
            if user_data:
                user = UserRegistrationSerializer(data=request.data)
                user.save()
                
                # add group customer
                customer_group, _ = Group.objects.get_or_create(name='Customer')
                user.groups.add(customer_group)

                # Generate tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_201_CREATED)

            return Response({"error": "User data not found. Please restart registration."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')

        if not email or not otp_code:
            return Response({"error": "Email and OTP code are required"}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = OTPCode.get_otp('otp', email)
        if stored_otp and stored_otp.decode() == otp_code:
            user, created = CustomUser.objects.get_or_create(email=email)
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)