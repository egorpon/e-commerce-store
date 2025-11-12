from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email has already been used")

        if len(email) > 350:
            raise forms.ValidationError("Your email is too long")

        return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        exclude = ['password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk):
            raise forms.ValidationError("This email has already been used")

        if len(email) > 350:
            raise forms.ValidationError("Your email is too long")

        return email