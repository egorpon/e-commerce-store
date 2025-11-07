from django.urls import path
from . import views

urlpatterns = [
    path("register/", view=views.register, name="register"),
    path(
        "email-verification/<str:uidb64>/<str:token>/",
        view=views.email_verification,
        name="email_verification",
    ),
    path(
        "email-verification-sent/",
        view=views.email_verification_sent,
        name="email_verification_sent",
    ),
    path(
        "email-verification-success/",
        view=views.email_verification_success,
        name="email_verification_success",
    ),
    path(
        "email-verification-failed/",
        view=views.email_verification_failed,
        name="email_verification_failed",
    ),
    path("login-user/", view=views.login_user, name="login_user"),
    path("logout-user/", views.logout_user, name="logout_user"),
    path("dashboard/", view=views.dashboard, name="dashboard"),
]
