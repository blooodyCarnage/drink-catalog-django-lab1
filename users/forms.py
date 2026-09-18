from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)

from .models import Profile


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(
            attrs={'class': 'form-input'}
        ),
    )

    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-input'}
        ),
    )


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'form-input'}
        ),
    )

    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-input'}
        ),
    )

    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-input'}
        ),
    )

    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-input'}
        ),
    )

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-input'}
        ),
    )

    password2 = forms.CharField(
        label='Повтор пароля',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-input'}
        ),
    )

    class Meta:
        model = get_user_model()

        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        user_model = get_user_model()

        if user_model.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                'Пользователь с таким E-mail уже существует.'
            )

        return email


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'form-input'}
        ),
    )

    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(
            attrs={'class': 'form-input'}
        ),
    )

    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-input'}
        ),
    )

    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-input'}
        ),
    )

    class Meta:
        model = Profile

        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'birth_date',
            'avatar',
            'bio',
        )

        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-input',
                }
            ),

            'bio': forms.Textarea(
                attrs={
                    'rows': 5,
                    'class': 'form-input',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            user = self.instance.user

            self.fields['username'].initial = (
                user.username
            )

            self.fields['email'].initial = (
                user.email
            )

            self.fields['first_name'].initial = (
                user.first_name
            )

            self.fields['last_name'].initial = (
                user.last_name
            )

    def clean_username(self):
        username = self.cleaned_data[
            'username'
        ].strip()

        user_model = get_user_model()

        queryset = user_model.objects.filter(
            username=username
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.user_id
            )

        if queryset.exists():
            raise forms.ValidationError(
                'Пользователь с таким логином уже существует.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data[
            'email'
        ].strip().lower()

        user_model = get_user_model()

        queryset = user_model.objects.filter(
            email__iexact=email
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.user_id
            )

        if queryset.exists():
            raise forms.ValidationError(
                'Пользователь с таким E-mail уже существует.'
            )

        return email

    def save(self, commit=True):
        profile = super().save(
            commit=False
        )

        user = profile.user

        user.username = self.cleaned_data[
            'username'
        ]

        user.email = self.cleaned_data[
            'email'
        ]

        user.first_name = self.cleaned_data[
            'first_name'
        ]

        user.last_name = self.cleaned_data[
            'last_name'
        ]

        if commit:
            user.save()
            profile.save()

        return profile


class UserPasswordChangeForm(
    PasswordChangeForm
):
    old_password = forms.CharField(
        label='Старый пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-input'}
        ),
    )

    new_password1 = forms.CharField(
        label='Новый пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-input'}
        ),
    )

    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-input'}
        ),
    )