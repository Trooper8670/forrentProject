from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Chat, Contact

User = get_user_model()


class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


def get_user_contact(first_name):
    user = get_object_or_404(User, first_name=first_name)
    return get_object_or_404(Contact, user=user)


class ChatSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants')
        read_only = 'id'

    def create(self, validated_data):
        print(validated_data)
        participants = validated_data.pop('participants')
        chat = Chat()
        chat.save()
        for first_name in participants:
            contact = get_user_contact(first_name)
            chat.participants.add(contact)
        chat.save()
        return chat
