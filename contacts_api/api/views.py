from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import viewsets
HEADERS_ERROR = {
    "data": {"message": "header is not provided"},
    "status": 404
}


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
            result = [{"id": c.id, "name": c.name, "created_at": c.created_at} for c in contact_groups]
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
            try:
                group = Group.objects.filter(id=data.get("group"), author=token["user_id"])
                group_id = group[0].id
                contact = Contact(
                    name=data.get("name"),
                    phone_number=data.get("phone_number"),
                    favorite=data.get("favorite"),
                    group=group_id,
                    author=token["user_id"]
                )
                contact.save()
                return Response({"message": "saved successfulfy"}, 201)
            except:
                return Response({"message": "Contact Group and User are not corresponding"}, 401)

        else:
            return Response(**HEADERS_ERROR)

    def list(self, request, *args, **kwargs):
        JWT_authenticator = self.authentication_classes[1]()
        response = JWT_authenticator.authenticate(request)

        if not response == None:
            user, token = response
            contact_users = Contact.objects.filter(author=token["user_id"])
            contact_list = [{
                "id": c.id,
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
