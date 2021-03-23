from django.contrib.sites.shortcuts import get_current_site
from requests import Response
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class ReadProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'email']

    def validate(self, attrs):
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only= True)


    class Meta:
        model = User
        fields = ['uid','email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')

        return attrs



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)


    class Meta:
        model= User
        fields = ['email',
                  'password']

    def validate(self, attrs):
        return attrs


class ForgotSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)



    class Meta:
        model =User
        fields= ['email']


    def validate(self, attrs):
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=68, min_length=6)




    class Meta:
        model = User
        fields = ['password', 'confirm_pass']


    class Meta:
        model = User
        fields = ['password', 'confirm_password']

