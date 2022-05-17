from email.mime import base
from rest_framework import routers

from . import views

app_name = "posts"
router = routers.DefaultRouter()

router.register("api/tags", views.TagViewSet, basename="tags")

urlpatterns = router.urls
