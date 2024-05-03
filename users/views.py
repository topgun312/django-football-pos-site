from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.forms import (
    LoginUserForm,
    ProfileUserForm,
    RegisterUserForm,
    UserPasswordChangeForm,
)

from football_site import settings


class LoginUser(LoginView):
    """
    Представление для авторизации пользователя
    """

    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}


def logout_user(request) -> HttpResponseRedirect:
    """
    Функция для выхода пользователя из системы
    """
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))


class RegisterUser(CreateView):
    """
    Представление для регистрации пользователя
    """

    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("users:login")


class ProfileUser(LoginRequiredMixin, UpdateView):
    """
    Представление для отобоажени и редактирования страницы пользователя
    """

    model = get_user_model()
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    extra_context = {
        "title": "Профиль пользователя",
        "default_image": settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    """
    Представление для изменения пароля пользователя
    """

    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
