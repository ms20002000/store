from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta
from discount.models import Coupon
from .models import Order
from .tasks import send_discount_email


@receiver(post_save, sender=Order)
def create_discount_coupon(sender, instance, created, **kwargs):
    """
    Signal to create a discount coupon and send it to the user's email after an order is created.
    """
    if created:  
        user = instance.user
        coupon = Coupon.objects.create(
            amount=30,  
            start_date=now(),
            expire_at=now() + timedelta(days=30),
            min_price=None,
            max_amount=None,
            user=user
        )
        coupon.save()

        send_discount_email.delay(
            email=user.email,
            coupon_code=coupon.code,
            expire_date=coupon.expire_at.strftime('%Y-%m-%d')
        )
