from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User

from .models import *


class TokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(TokenPairSerializer, self).validate(attrs)
        data["groups"] = [
            {"id": group.id, "name": group.name} for group in self.user.groups.all()
        ]
        data["is_superuser"] = self.user.is_superuser
        data["id"] = self.user.id
        data["username"] = self.user.username
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "last_name",
            "first_name",
            "email",
            "groups",
        )
        extra_kwargs = {
            "username": {"validators": [UnicodeUsernameValidator()]},
            "password": {"write_only": True},
        }


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "name",


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "name", "number", "favorite", "group"
