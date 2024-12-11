from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-register/', VerifyRegisterView.as_view(), name='verify_register'),
    path('login/', LoginView.as_view(), name='login'),
]