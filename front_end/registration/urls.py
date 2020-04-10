from django.contrib.auth import views as auth_views
from django.urls import path

from registration import views

app_name = 'registration'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('change_password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]