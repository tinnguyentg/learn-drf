from django.urls import include, path

from . import views


app_name = "users"
urlpatterns = [path("api/", include("users.urls_api", namespace="api"))]
