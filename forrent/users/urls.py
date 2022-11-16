from django.urls import path
from .views import (
    EmailRegisterView,
    PhoneRegisterView,
    EmailLogin,
    PhoneLogin,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/login/by-email/', EmailLogin.as_view(), name='email_login'),
    path('api/login/by-phone/', PhoneLogin.as_view(), name='phone_login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/by-email/', EmailRegisterView.as_view(), name="email_sign_up"),
    path('api/register/by-phone/', PhoneRegisterView.as_view(), name="phone_sign_up"),
]
