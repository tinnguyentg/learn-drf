import factory
from faker import Faker

from users.models import CustomUser

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.lazy_attribute(lambda _: fake.unique.email())


class AdminFactory(UserFactory):
    is_verified = True
    is_staff = True
    is_superuser = True
