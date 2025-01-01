from django.urls import path
from .views import *

urlpatterns = [
    path('use_coupon/', UseCouponView.as_view(), name='use_coupon'),
]