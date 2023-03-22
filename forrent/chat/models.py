from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    """
    Класс контакта пользователя чата.
    The contact class of the chat user.
    """
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.first_name


class Message(models.Model):
    """
    Класс сообщения пользователя чата.
    The chat user's message class.
    """
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.first_name


class Chat(models.Model):
    """
    Класс пользователя чата.
    The chat user class.
    """
    participants = models.ManyToManyField(Contact, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)
