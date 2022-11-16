from abc import ABC
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


class Login(APIView, TokenObtainPairSerializer, ABC):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def post(self, request):
        email = request.data.get("email")
        phone = request.data.get("phone")
        password = request.data.get("password")

        if not email:
            check_phone = User.objects.filter(phone=phone).exist()
            if not check_phone:
                return Response({"error": "Phone does not exists"}, status=status.HTTP_404_NOT_FOUND)

            phone_user = authenticate(phone=phone, password=password)
            if phone_user is not None:
                login(request, phone_user)
                token = super().get_token(phone_user)
                data = {
                    "token": token.key,
                    "phone_user_id": request.phone_user.pk,
                    "phone": request.user.phone
                }
                return Response({"success": "Successfully login", "data": data}, status=status.HTTP_200_OK)

        if not phone:
            check_email = User.objects.filter(email=email).exist()
            if not check_email:
                return Response({"error": "Email does not exists"}, status=status.HTTP_404_NOT_FOUND)

            email_user = authenticate(email=email, password=password)
            if email_user is not None:
                login(request, email_user)
                token = super().get_token(email_user)
                data = {
                    "token": token.key,
                    "email_user_id": request.email_user.pk,
                    "email": request.user.email
                }
                return Response({"success": "Successfully login", "data": data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid login details"}, status=status.HTTP_400_BAD_REQUEST)