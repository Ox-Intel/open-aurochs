from django.contrib.auth.forms import (
    PasswordResetForm,
    AuthenticationForm,
    SetPasswordForm,
)
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.views import LoginView
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from annoying.decorators import render_to
from utils.encryption import lookup_hash
from organizations.models import User


class AurochsLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""
        self.fields["username"].widget.attrs.update(
            {
                "class": "ox-login-input input input-bordered w-48 mb-2 mt-4",
                "placeholder": "Email or Username",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "ox-login-input input input-bordered w-48 ",
                "placeholder": "Password",
            }
        )


class AurochsLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AurochsPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = User.objects.filter(email=email)
        return (u for u in active_users if u.has_usable_password())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ""
        self.fields["email"].widget.attrs.update(
            {
                "class": "ox-login-input input input-bordered w-48 mb-2 mt-4",
                "placeholder": "Email",
            }
        )


class AurochsPasswordResetView(PasswordResetView):
    form_class = AurochsPasswordResetForm


class AurochsPasswordConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        self.fields["new_password1"].label = ""
        self.fields["new_password2"].label = ""
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "join-item input input-bordered w-48 mb-2 mt-4",
                "placeholder": "New Password",
                "autofocus": "true",
            }
        )
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "join-item input input-bordered w-48 ",
                "placeholder": "Confirm Password",
            }
        )


class AurochsPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = AurochsPasswordConfirmForm


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        u = None
        try:
            # check if the user is trying to login with their email address
            for u in User.objects.filter(email=username).all():
                if u.check_password(password):
                    return u
        except:
            pass

        # if the user is not an email, we assume it's a username
        try:
            u = User.objects.get(username=username)
            if u.check_password(password):
                return u
        except User.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
