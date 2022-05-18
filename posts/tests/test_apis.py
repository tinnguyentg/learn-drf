from random import choice
import factory
from django.urls import reverse

from rest_framework.test import APITestCase
from posts.models import Post, Tag
from posts.serializers import TagListCreateSerializer

from users.tests.factories import UserFactory

from .factories import TagFactory, PostFactory
from learndrf.tests.base import BaseAPITestCase


class TestTagViewSet(APITestCase, BaseAPITestCase):
    def setUp(self):
        self.data = factory.build(dict, FACTORY_CLASS=TagFactory)
        self.urls = {
            "list": reverse("posts:tags-list"),
            "detail": lambda slug: reverse("posts:tags-detail", args=(slug,)),
        }
        self.user = UserFactory()
        self.auth()

    def auth(self):
        self.session(self.user)

    def test_get_list(self):
        tags = TagFactory.create_batch(10)
        response = self.client.get(self.urls["list"])
        self.assertSuccess(response)
        self.assertEqual(len(tags), len(response.data))

    def test_create_tag_fail(self):
        self.client.logout()
        self.client.credentials()
        response = self.client.post(self.urls["list"], data=self.data)
        self.assertForbidden(response)

    def test_create_tag(self):
        response = self.client.post(self.urls["list"], data=self.data)
        self.assertCreated(response)

    def test_creat_duplicate(self):
        tag = TagFactory()
        self.data["name"] = tag.name
        response = self.client.post(self.urls["list"], self.data)
        self.assertBadRequest(response)

    def test_detail_tag(self):
        tag = TagFactory()
        PostFactory.create_batch(2, tags=[tag])
        url = self.urls["detail"](tag.slug)
        response = self.client.get(url)
        self.assertSuccess(response)
        self.assertKeysInReponseData(response, ["name", "slug", "posts"])


class TestTagViewSetWithAuthToken(TestTagViewSet):
    def auth(self):
        self.token(self.user)


class TestTagViewSetWithJWTToken(TestTagViewSet):
    def auth(self):
        self.jwt(self.user)


class TestPostViewSet(APITestCase, BaseAPITestCase):
    def setUp(self) -> None:
        self.urls = {
            "list": reverse("posts:posts-list"),
            "detail": lambda slug: reverse("posts:posts-detail", args=(slug,)),
        }
        self.user = UserFactory()
        self.auth()

        self.data = factory.build(dict, FACTORY_CLASS=PostFactory)
        del self.data["author"]

    def auth(self):
        self.session(self.user)

    def test_create_post(self):
        response = self.client.post(self.urls["list"], self.data)
        self.assertCreated(response)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.get()
        self.assertEqual(post.title, response.data["title"])

    def test_create_post_with_tags(self):
        tags_data = factory.build_batch(dict, FACTORY_CLASS=TagFactory, size=3)
        self.data["tags"] = tags_data
        response = self.client.post(self.urls["list"], data=self.data)
        self.assertCreated(response)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.get()
        self.assertEqual(post.title, response.data["title"])
        self.assertEqual(post.tags.count(), len(tags_data))

    def test_create_post_with_duplicate_tags(self):
        tags = TagFactory.create_batch(2)
        tags_data = TagListCreateSerializer(tags, many=True)
        self.data["tags"] = tags_data.data
        response = self.client.post(self.urls["list"], self.data)
        self.assertCreated(response)

    def test_retrieve_post(self):
        tags = TagFactory.create_batch(3)
        post = PostFactory(tags=tags)
        url = self.urls["detail"](post.slug)
        response = self.client.get(url)
        self.assertSuccess(response)

    def test_update_post(self):
        post = PostFactory()
        self.user = post.author
        self.auth()
        url = self.urls["detail"](post.slug)
        title = post.title
        response = self.client.put(url, self.data)
        self.assertSuccess(response)
        post.refresh_from_db()
        self.assertNotEqual(title, post.title)

    def test_update_post_tags(self):
        tags = TagFactory.create_batch(3)
        post = PostFactory(tags=tags)
        self.user = post.author
        self.auth()
        url = self.urls["detail"](post.slug)
        new_tags = factory.build_batch(dict, 3, FACTORY_CLASS=TagFactory)
        self.data["tags"] = new_tags
        response = self.client.put(url, self.data)
        self.assertSuccess(response)
        self.assertEqual(Tag.objects.count(), 6)

    def test_remove_post_tags(self):
        tags = TagFactory.create_batch(3)
        post = PostFactory(tags=tags)
        self.user = post.author
        self.auth()
        url = self.urls["detail"](post.slug)
        self.data["tags"] = []
        response = self.client.put(url, self.data)
        self.assertSuccess(response)
        self.assertEqual(response.data["tags"], [])

    def test_update_post_with_patch(self):
        tags = TagFactory.create_batch(3)
        post = PostFactory(tags=tags)
        self.user = post.author
        self.auth()
        url = self.urls["detail"](post.slug)
        data = {"title": "123"}
        response = self.client.patch(url, data)
        self.assertSuccess(response)
        self.assertEqual(response.data["title"], data["title"])
