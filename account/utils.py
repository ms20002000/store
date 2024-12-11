from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(email, otp_code):
    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp_code}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
