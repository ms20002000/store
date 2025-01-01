from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_discount_email(email, coupon_code, expire_date):
    """
    Celery task to send a discount email.
    """
    subject = "Your 30% Discount Code"
    message = (
        f"Thank you for your order! Here is your 30% discount code: {coupon_code}. "
        f"This code is valid until {expire_date}."
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
