import factory
from faker import Faker

from users.models import CustomUser

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.lazy_attribute(lambda _: fake.unique.email())
    password = "dsakj#@*ASHD"

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.set_password(obj.password)
        obj.save()

class AdminFactory(UserFactory):
    is_verified = True
    is_staff = True
    is_superuser = True
