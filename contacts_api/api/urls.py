from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt import views as jwt_views
from .views import *

router = routers.DefaultRouter()
router.register("Group", GroupViewSet)
router.register("Contact", ContactViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path('login/', TokenPairView.as_view()),
    path("api-auth/", include("rest_framework.urls")),
     path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]