from django.urls import path
from .views import *

urlpatterns = [
    path('create_order/', CreateOrderView.as_view(), name='create-order'),
    path('order_history/', UserOrderListView.as_view(), name='order-history'),
    path('check-purchased-products/', CheckPurchasedProductsView.as_view(), name='check-purchased-products'),
]