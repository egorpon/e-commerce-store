from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CreateUserForm, LoginUserForm

from django.contrib.sites.shortcuts import get_current_site

from .token import email_token_generator

from django.contrib.auth.models import User
# Create your views here.

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


from django.contrib.auth import authenticate, login, logout


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = "Account verification email"
            message = render_to_string(
                "account/registration/email-verification.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": email_token_generator.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)

            return redirect("email_verification_sent")
        else:
            print(form.errors)

    context = {"form": form}

    return render(request, "account/registration/register.html", context=context)


def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    if user and email_token_generator.check_token(user, token):
        user.is_active = True

        user.save()

        return redirect("email_verification_success")
    else:
        return redirect("email_verification_failed")


def email_verification_sent(request):
    return render(request, "account/registration/email-verification-sent.html")


def email_verification_success(request):
    return render(request, "account/registration/email-verification-success.html")


def email_verification_failed(request):
    return render(request, "account/registration/email-verification-failed.html")


def login_user(request):
    form = LoginUserForm()
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
        else:
            print(form.non_field_errors())

    context = {"form": form}
    return render(request, "account/login_user.html", context=context)


def logout_user(request):
    logout(request)
    return redirect("store")


def dashboard(request):
    return render(request, "account/dashboard.html")
