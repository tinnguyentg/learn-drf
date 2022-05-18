from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from users.tests.factories import UserFactory


class BaseAPITestCase:
    def assertStatus(self, response, status):
        self.assertEqual(response.status_code, status)

    def assertBadRequest(self, response):
        self.assertStatus(response, status.HTTP_400_BAD_REQUEST)

    def assertForbidden(self, response):
        self.assertStatus(response, status.HTTP_403_FORBIDDEN)

    def assertCreated(self, response):
        self.assertStatus(response, status.HTTP_201_CREATED)

    def assertSuccess(self, response):
        self.assertStatus(response, status.HTTP_200_OK)

    def assertKeysInReponseData(self, response, keys):
        data = response.data
        for key in keys:
            self.assertIn(key, data)

    def session(self, user):
        credentials = {"email": user.email, "password": UserFactory.password}
        self.client.login(**credentials)

    def token(self, user):
        self.client.credentials(HTTP_AUTHORIZATION="Token %s" % user.auth_token)

    def jwt(self, user):
        token = RefreshToken.for_user(user)
        access = str(token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % access)
