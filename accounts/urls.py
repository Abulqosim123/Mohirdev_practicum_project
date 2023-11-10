from django.urls import path, reverse_lazy
from .views import profile
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

from . import views
from .views import user_login, dashboard_view, SignUpView, edit_user, EditUserView

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('password_change/', PasswordChangeView.as_view(template_name='registration/change_password_form.html'),
         name='password_change'),
    path('password_change/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
    path(
        'reset-password/',
        PasswordResetView.as_view(template_name='registration/password_reset.form.html'),
        name='reset_password'),

    path(
        'reset-password-done/',
        PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path(
        'reset-password/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path(
        'reset-password-complete/',
        PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),

    path('profile/', dashboard_view, name='user_profile'),
    path('register/', views.register, name='register'),
    # path('profile/edit/', edit_user, name='edit_user_information'),
    path('profile/edit/', EditUserView.as_view(), name='edit_user_information'),

]
