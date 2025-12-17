from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

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
    path(
        "profile-management/", view=views.profile_management, name="profile_management"
    ),
    path("delete/", view=views.delete_account, name="delete_account"),
    path(
        "reset-password/",
        view=auth_views.PasswordResetView.as_view(
            template_name="account/password/password-reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset-password-sent/",
        view=auth_views.PasswordResetDoneView.as_view(
            template_name="account/password/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<str:uidb64>/<str:token>/",
        view=auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password-reset-form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password-complete/",
        view=auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    path("manage-shipping/", view=views.manage_shipping, name="manage_shipping"),
    path("my-orders/", view=views.my_orders, name="my_orders"),
]
