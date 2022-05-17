from .factories import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken


def token_auth(client, user):
    client.credentials(HTTP_AUTHORIZATION="Token %s" % user.auth_token)


def jwt_auth(client, user):
    token = RefreshToken.for_user(user)
    access = str(token.access_token)
    client.credentials(HTTP_AUTHORIZATION="Bearer %s" % access)


def session_auth(client, user):
    credentials = {"email": user.email, "password": UserFactory.password}
    client.login(**credentials)
