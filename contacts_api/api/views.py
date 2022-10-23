from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from .models import *
from rest_framework import mixins
from rest_framework import viewsets
from django.http import Http404
HEADERS_ERROR = {
    "data": {"message": "header is not provided"},
    "status": 404
}
# from datetime import datetime, timedelta, date


class TokenPairView(TokenObtainPairView):
    serializer_class = TokenPairSerializer


class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = SessionAuthentication, JWTAuthentication
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        JWT_authenticator = self.authentication_classes[1]()
        response = JWT_authenticator.authenticate(request)
        data = request.data

        if not response == None:
            _, token = response
            group = Group(
                author=token["user_id"],
                name=data.get("name"),
            )
            group.save()
        else:
            return Response(**HEADERS_ERROR)

    def list(self, request, *args, **kwargs):
        JWT_authenticator = self.authentication_classes[1]()

        response = JWT_authenticator.authenticate(request)
        if not response == None:
            user, token = response
            contact_groups = Group.objects.filter(author=token["user_id"])
            result = [{"name": c.name, "created_at": c.created_at} for c in contact_groups]
            return Response(data=result, status=200)
        else:
            return Response(**HEADERS_ERROR)


class ContactViewSet(viewsets.ModelViewSet):
    authentication_classes = SessionAuthentication, JWTAuthentication
    permission_classes = (IsAuthenticated,)
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        JWT_authenticator = self.authentication_classes[1]()
        response = JWT_authenticator.authenticate(request)
        data = request.data
        if not response == None:
            _, token = response
            contact = Contact(
                name=data.get("name"),
                phone_number=data.get("phone_number"),
                favorite=data.get("favorite"),
                group=data.get("group"),
                author=token["user_id"]
            )
            contact.save()
            return Response({"message": "saved successfulfy"}, 201)

        else:
            return Response(**HEADERS_ERROR)

    def list(self, request, *args, **kwargs):
        JWT_authenticator = self.authentication_classes[1]()
        response = JWT_authenticator.authenticate(request)

        if not response == None:
            user, token = response
            contact_users = Contact.objects.filter(author=token["user_id"])
            contact_list = [{
                "name": c.name,
                "phone_number": c.number,
                "favorite": c.favorite,
                "created_at": c.created_at,
                "group": {"group_name": c.group.name}
            } for c in contact_users if token["user_id"] == c.group.author.id]

            # print(contact_list)

            return Response(contact_list, 200)

        else:
            return Response(**HEADERS_ERROR)
