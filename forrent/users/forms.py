from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from .models import *


class EmailAuthenticationForm(DjangoAuthenticationForm):

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request,
                email=email,
                password=password,
            )
            if not self.user_cache.email_verify:
                raise ValidationError(
                    'Email not verify, check your email',
                    code='invalid_login',
                )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class PhoneAuthenticationForm(DjangoAuthenticationForm):

    def clean(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')

        if phone is not None and password:
            self.user_cache = authenticate(
                self.request,
                phone=phone,
                password=password,
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class EmailUserRegister(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(EmailUserRegister, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class PhoneUserRegister(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(PhoneUserRegister, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name']


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

