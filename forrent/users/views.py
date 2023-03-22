from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import PhoneUserSerializer
from rest_framework import generics
from django.middleware.csrf import get_token
from django.views.decorators.http import require_POST
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User


def get_csrf(request):
    response = Response({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response


@require_POST
def login_view(request):
    phone = request.get('phone')
    password = request.get('password')

    if phone is None or password is None:
        return Response({'detail': 'Please provide phone and password.'}, status=400)

    user = authenticate(phone=phone, password=password)

    if user is None:
        return Response({'detail': 'Invalid credentials.'}, status=400)

    login(request, user)
    return Response({'detail': 'Successfully logged in.'})


def logout_view(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)
    return Response({'detail': 'Successfully logged out.'})


class SessionView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return Response({'isAuthenticated': True})


class PhoneRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PhoneUserSerializer
