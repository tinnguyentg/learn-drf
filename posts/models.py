from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


UserModel = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, editable=False)

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super().save(**kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, editable=False)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super().save(**kwargs)

    def __str__(self):
        return self.title
