from django.urls import path, include
from .views import PhoneRegisterView
from . import views

urlpatterns = [
    path('api/login/', views.login_view, name='api-login'),
    path('api/logout/', views.logout_view, name='api-logout'),
    path('api/register/', PhoneRegisterView.as_view(), name="phone_sign_up"),
    path('api/csrf/', views.get_csrf, name='api-csrf'),
    path('api/session/', views.SessionView.as_view(), name='api-session'),

    path('accounts/', include('allauth.urls')),
]
