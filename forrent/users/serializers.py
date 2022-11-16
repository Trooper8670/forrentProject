from rest_framework import serializers
from .models import User


class EmailUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

        @staticmethod
        def create(validated_data):
            user = User.objects.create(email=validated_data['email'],
                                       first_name=validated_data['first_name']
                                       )
            user.set_password(validated_data['password'])
            user.save()
            return user


class PhoneUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'password']

        @staticmethod
        def create(validated_data):
            user = User.objects.create(phone=validated_data['phone'],
                                       first_name=validated_data['first_name']
                                       )
            user.set_password(validated_data['password'])
            user.save()
            return user
