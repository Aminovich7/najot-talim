from decimal import Decimal

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from users.constants import PREMIUM_SUBSCRIPTION_PRICE
from users.models import CustomUser


class SignupViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("signup")
        self.valid_data = {
            "username": "nozim21",
            "email": "qahorov@example.com",
            "first_name": "Nozim",
            "last_name": "Qahorov",
            "profession": "driver",
            "password": "Pass123test!",
            "password_confirm": "Pass123test!",
        }

    def test_signup_success(self):
        response = self.client.post(self.url, self.valid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "nozim21")

    def test_signup_invalid_email(self):
        data = {**self.valid_data, "email": "bad@x"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_password_mismatch(self):
        data = {**self.valid_data, "password_confirm": "WrongPass123!"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("login")
        self.user = CustomUser.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="Pass123test!",
            profession="driver",
            first_name="Login",
            last_name="User",
        )

    def test_login_success(self):
        data = {"username": "loginuser", "password": "Pass123test!"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "loginuser")

    def test_login_wrong_password(self):
        data = {"username": "loginuser", "password": "WrongPass123!"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_username(self):
        data = {"username": "unknown", "password": "Pass123test!"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("logout")
        self.user = CustomUser.objects.create_user(
            username="logoutuser",
            email="logout@example.com",
            password="Pass123test!",
            profession="driver",
            first_name="Logout",
            last_name="User",
        )
        self.token = Token.objects.create(user=self.user)

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Tizimdan muvaffaqiyatli chiqildi.")

    def test_logout_unauthenticated(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_deletes_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.client.post(self.url)

        self.assertFalse(Token.objects.filter(user=self.user).exists())


class ProfileApiViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("profile")
        self.user = CustomUser.objects.create_user(
            username="profileuser",
            email="profile@example.com",
            password="Pass123test!",
            profession="driver",
            first_name="Profile",
            last_name="User",
        )
        self.token = Token.objects.create(user=self.user)

    def test_profile_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "profileuser")

    def test_profile_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_contains_wallet(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.get(self.url)

        self.assertIn("wallet", response.data)
        self.assertEqual(str(response.data["wallet"]["balance"]), "0.00")


class UpdateProfileApiViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("profile-update")
        self.user = CustomUser.objects.create_user(
            username="updateuser",
            email="update@example.com",
            password="Pass123test!",
            profession="driver",
            first_name="Update",
            last_name="User",
        )
        self.token = Token.objects.create(user=self.user)

    def test_update_profile_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {"first_name": "Updated"}

        response = self.client.put(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")

    def test_update_profile_unauthenticated(self):
        response = self.client.put(self.url, {"first_name": "Updated"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChangePasswordApiViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("change-password")
        self.user = CustomUser.objects.create_user(
            username="passuser",
            email="pass@example.com",
            password="Pass123test!",
            profession="driver",
            first_name="Pass",
            last_name="User",
        )
        self.token = Token.objects.create(user=self.user)

    def test_change_password_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {
            "old_password": "Pass123test!",
            "new_password": "NewPass123test!",
            "new_password_confirm": "NewPass123test!",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass123test!"))

    def test_change_password_wrong_old_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {
            "old_password": "WrongPass123!",
            "new_password": "NewPass123test!",
            "new_password_confirm": "NewPass123test!",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db()
class UserDeletePytest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("account-delete")
        self.user = CustomUser.objects.create_user(
            username="deleteuser",
            email="delete@example.com",
            password="Pass123test!",
            profession="driver",
            first_name="Delete",
            last_name="User",
        )
        self.token = Token.objects.create(user=self.user)

    def test_delete_account_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {"password": "Pass123test!"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(CustomUser.objects.filter(username="deleteuser").exists())

    def test_delete_account_wrong_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {"password": "WrongPass123!"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db()
class BuyPremiumPytest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("buy-premium")
        self.user = CustomUser.objects.create_user(
            username="premiumuser",
            email="premium@example.com",
            password="Pass123test!",
            profession="driver",
            first_name="Premium",
            last_name="User",
        )
        self.token = Token.objects.create(user=self.user)

    def test_buy_premium_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.user.wallet.balance = Decimal(str(PREMIUM_SUBSCRIPTION_PRICE))
        self.user.wallet.save()

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_premium)

    def test_buy_premium_insufficient_balance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Mablag' yetarli emas!")

