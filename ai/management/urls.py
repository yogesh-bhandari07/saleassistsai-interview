
from django.urls import path
from management.views import *
urlpatterns = [
  


    path('user/register', UserRegistrationView.as_view(), name='register'),
    path('user/login', UserLoginView.as_view(), name='login'),
    path('user/profile', UserProfileView.as_view(), name='profile'),
    path('user/changepassword', UserChangePasswordView.as_view(), name='changepassword'),
    path('user/send-reset-password-email', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('user/reset-password/<uid>/<token>', UserPasswordResetView.as_view(), name='reset-password'),


    path('products', ProductsView.as_view(), name='products'),
    path('products/<int:pk>', ProductsView.as_view(), name='products'),



]
