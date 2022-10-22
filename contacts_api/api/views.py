# from datetime import datetime, timedelta, date
from django.http import Http404
from rest_framework import viewsets
from rest_framework import mixins
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend




class TokenPairView(TokenObtainPairView):
    serializer_class = TokenPairSerializer

class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = SessionAuthentication, JWTAuthentication
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def list(self, request, *args, **kwargs):
        JWT_authenticator = self.authentication_classes[1]()


        response = JWT_authenticator.authenticate(request)
        if not response == None:
            user, token = response
            contact_groups = Group.objects.filter(author=token["user_id"])
            result = [{"name": c.name} for c in contact_groups]
            return Response(data=result, status=200)
        else:
            return Response(data={"message": "header is not provided"}, status=404)

class ContactViewSet(viewsets.ModelViewSet):
    authentication_classes = SessionAuthentication, JWTAuthentication
    permission_classes = (IsAuthenticated,)
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

