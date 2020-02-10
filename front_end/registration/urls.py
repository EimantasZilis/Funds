from django.contrib.auth import views as auth_views
from django.urls import path

from registration import views

app_name = 'registration'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logged_in/', views.LoggedInView.as_view(), name='logged_in'),
    path('logged_out/', views.LoggedOutView.as_view(), name='logged_out'),
    path('signup/', views.SignupView.as_view(), name='signup'),    
]