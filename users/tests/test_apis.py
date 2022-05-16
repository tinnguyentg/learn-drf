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