from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-register/', VerifyOTPView.as_view(), name='verify_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login_password/', LoginPasswordView.as_view(), name='login_password'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('user/products/', UserPurchasedProductsView.as_view(), name='user-purchased-products'),
]