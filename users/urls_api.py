from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
]
