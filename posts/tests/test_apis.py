from random import choice
import factory
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Tag, Post

from users.tests.factories import UserFactory

from .factories import TagFactory, PostFactory
from users.tests import auth


class TestTagViewSet(APITestCase):
    def setUp(self):
        self.tags = TagFactory.create_batch(10)
        PostFactory.create_batch(2, tags=self.tags)
        self.new_tag_data = factory.build(dict, FACTORY_CLASS=TagFactory)
        self.urls = {
            "list": reverse("posts:tags-list"),
            "detail": lambda slug: reverse("posts:tags-detail", args=(slug,)),
        }
        self.user = UserFactory()
        self.auth()

    def auth(self):
        auth.session_auth(self.client, self.user)

    def test_get_list(self):
        response = self.client.get(self.urls["list"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.tags), len(response.data))

    def test_create_tag_fail(self):
        self.client.logout()
        self.client.credentials()
        response = self.client.post(self.urls["list"], data=self.new_tag_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_tag(self):
        response = self.client.post(self.urls["list"], data=self.new_tag_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_tag(self):
        tag = choice(self.tags)
        url = self.urls["detail"](tag.slug)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], tag.name)
        self.assertEqual(response.data["slug"], tag.slug)
        self.assertIn("posts", response.data)


class TestTagViewSetWithAuthToken(TestTagViewSet):
    def auth(self):
        auth.token_auth(self.client, self.user)


class TestTagViewSetWithJWTToken(TestTagViewSet):
    def auth(self):
        auth.jwt_auth(self.client, self.user)


class TestPostViewSet(APITestCase):
    def setUp(self) -> None:
        self.data = factory.build(dict, FACTORY_CLASS=PostFactory)
        self.user = UserFactory()
        del self.data["author"]
        self.urls = {"list": reverse("posts:posts-list")}
        self.auth()

    def auth(self):
        auth.session_auth(self.client, self.user)

    def test_create_post(self):
        response = self.client.post(self.urls["list"], self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.get()
        self.assertEqual(post.title, response.data["title"])
