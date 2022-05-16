import factory
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import UserFactory

UserModel = get_user_model()


class TestSignUpView(APITestCase):
    def setUp(self):
        self.url = reverse("users:api:signup")
        self.data = factory.build(dict, FACTORY_CLASS=UserFactory)

    def test_signup(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserModel.objects.count(), 1)

    def test_email_exist(self):
        UserFactory(**self.data)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_weak_password(self):
        self.data.update({"password": "123"})
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)


class TestLoginView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("users:api:login")
        self.user = UserFactory()
        self.credentials = {"email": self.user.email, "password": UserFactory.password}

    def test_login(self):
        response = self.client.post(self.url, data=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail(self):
        credentials = factory.build(dict, FACTORY_CLASS=UserFactory)
        response = self.client.post(self.url, data=credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestPasswordChangeView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("users:api:password_change")
        self.user = UserFactory()
        self.credentials = {"email": self.user.email, "password": UserFactory.password}

    def test_password_change(self):
        data = {"current": UserFactory.password, "new": "zxc,nm,#@12"}
        self.client.login(**self.credentials)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(data["new"]))

    def test_password_change_fail(self):
        data = {"current": UserFactory.password, "new": "zxc,nm,#@12"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_current_password(self):
        data = {"current": "123", "new": "zxc,nm,#@12"}
        self.client.login(**self.credentials)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_new_password(self):
        data = {"current": UserFactory.password, "new": "123"}
        self.client.login(**self.credentials)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_change_using_token_authentication(self):
        data = {"current": UserFactory.password, "new": "zxc,nm,#@12"}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(data["new"]))
