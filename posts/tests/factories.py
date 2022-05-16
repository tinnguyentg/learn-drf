from random import choice

import factory
from faker import Faker
from mdgen import MarkdownPostProvider

from posts.models import Post, Tag
from users.tests.factories import UserFactory

fake = Faker()
fake.add_provider(MarkdownPostProvider)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.lazy_attribute(lambda _: fake.unique.word())


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.lazy_attribute(lambda _: fake.unique.paragraph(1))
    content = factory.lazy_attribute(
        lambda _: fake.post(choice(["small", "medium", "large"]))
    )
    author = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag in extracted:
                self.tags.add(tag)
