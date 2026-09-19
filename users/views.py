from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    TemplateView,
    UpdateView,
)

from .forms import (
    LoginUserForm,
    RegisterUserForm,
    UserPasswordChangeForm,
    UserProfileForm,
)
from .models import Profile
from drinks.models import Drink

from django.contrib.auth.forms import (
    AuthenticationForm,
)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    extra_context = {
        'title': 'Авторизация'
    }

    def get_success_url(self):
        return (
            self.get_redirect_url()
            or reverse_lazy('home')
        )


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy(
        'users:login'
    )

    extra_context = {
        'title': 'Регистрация'
    }


class ProfileUser(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = 'users/profile.html'

    extra_context = {
        'title': 'Профиль пользователя'
    }

    def get_context_data(
        self,
        **kwargs,
    ):
        context = super().get_context_data(
            **kwargs
        )

        profile, _ = (
            Profile.objects.get_or_create(
                user=self.request.user
            )
        )

        context['profile'] = profile

        context['reposted_drinks'] = (
            Drink.objects
            .filter(reposted_by=self.request.user)
            .select_related('category', 'author')
            .prefetch_related('tags')
        )

        return context


class EditProfileUser(
    LoginRequiredMixin,
    UpdateView,
):
    model = Profile
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'

    success_url = reverse_lazy(
        'users:profile'
    )

    extra_context = {
        'title': 'Редактирование профиля'
    }

    def get_object(
        self,
        queryset=None,
    ):
        profile, _ = (
            Profile.objects.get_or_create(
                user=self.request.user
            )
        )

        return profile


class UserPasswordChange(
    LoginRequiredMixin,
    PasswordChangeView,
):
    form_class = UserPasswordChangeForm

    template_name = (
        'users/password_change.html'
    )

    success_url = reverse_lazy(
        'users:profile'
    )

    extra_context = {
        'title': 'Смена пароля'
    }