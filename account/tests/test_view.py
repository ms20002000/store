import pytest
from rest_framework.test import APIClient
from rest_framework import status
from account.models import CustomUser
from account.redis import OTPCode


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "1234567890",
        "password": "testpassword123",
    }


@pytest.fixture
def create_user(user_data):
    return CustomUser.objects.create_user(**user_data)


# Test RegisterView
def test_register_view_get(api_client):
    response = api_client.get("/account/register/")
    assert response.status_code == status.HTTP_200_OK
    assert "fields" in response.data
    assert "instructions" in response.data


def test_register_view_post_valid(api_client, user_data, mocker):
    mocker.patch("account.redis.OTPCode.generate_code", return_value="123456")
    mocker.patch("account.utils.send_otp_email.delay")

    response = api_client.post("/account/register/", data=user_data)
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.data
    OTPCode.save_otp_to_redis.assert_called_once_with(user_data["email"], "123456")


def test_register_view_post_invalid(api_client):
    invalid_data = {"email": "invalid-email"}
    response = api_client.post("/account/register/", data=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


# Test VerifyOTPView
def test_verify_otp_view_post_valid(api_client, user_data, mocker):
    mocker.patch("account.redis.OTPCode.get_otp_code", return_value="123456")
    mocker.patch("account.redis.OTPCode.get_user_data", return_value=user_data)

    OTPCode.save_user_data_to_redis(user_data["email"], user_data)
    response = api_client.post(
        "/account/verify-otp/",
        data={"email": user_data["email"], "otp_code": "123456", "is_login_code": "false"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert "refresh" in response.data


def test_verify_otp_view_post_invalid_otp(api_client, user_data, mocker):
    mocker.patch("account.redis.OTPCode.get_otp_code", return_value="654321")

    response = api_client.post(
        "/account/verify-otp/",
        data={"email": user_data["email"], "otp_code": "123456"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


# Test LoginView
def test_login_view_post_valid(api_client, create_user, mocker):
    mocker.patch("account.redis.OTPCode.generate_code", return_value="123456")
    mocker.patch("account.utils.send_otp_email.delay")

    response = api_client.post("/account/login/", data={"email": create_user.email})
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.data
    OTPCode.save_otp_to_redis.assert_called_once_with(create_user.email, "123456")


def test_login_view_post_invalid(api_client):
    response = api_client.post("/account/login/", data={"email": "nonexistent@example.com"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "error" in response.data


# Test EditProfileView
def test_edit_profile_view_get(api_client, create_user):
    api_client.force_authenticate(user=create_user)
    response = api_client.get("/account/edit-profile/")
    assert response.status_code == status.HTTP_200_OK
    assert "email" in response.data


def test_edit_profile_view_put(api_client, create_user):
    api_client.force_authenticate(user=create_user)
    updated_data = {"first_name": "Jane", "last_name": "Smith"}
    response = api_client.put("/account/edit-profile/", data=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Jane"
    assert response.data["last_name"] == "Smith"


# Test UserPurchasedProductsView
def test_user_purchased_products_view(api_client, create_user):
    api_client.force_authenticate(user=create_user)
    response = api_client.get("/account/purchased-products/")
    assert response.status_code == status.HTTP_200_OK
    assert "products" in response.data
