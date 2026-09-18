from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views


app_name = 'users'

urlpatterns = [
    path(
        'login/',
        views.LoginUser.as_view(),
        name='login',
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),

    path(
        'register/',
        views.RegisterUser.as_view(),
        name='register',
    ),

    path(
        'profile/',
        views.ProfileUser.as_view(),
        name='profile',
    ),

    path(
        'profile/edit/',
        views.EditProfileUser.as_view(),
        name='profile_edit',
    ),

    path(
        'password-change/',
        views.UserPasswordChange.as_view(),
        name='password_change',
    ),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            email_template_name='users/password_reset_email.html',
            subject_template_name='users/password_reset_subject.txt',
            success_url=reverse_lazy(
                'users:password_reset_done'
            ),
        ),
        name='password_reset',
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy(
                'users:password_reset_complete'
            ),
        ),
        name='password_reset_confirm',
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]