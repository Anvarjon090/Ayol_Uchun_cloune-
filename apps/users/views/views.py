from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import Interest, UserCourse, UserWebinar
from apps.users.serializers import (
    InterestSerializer,
    UserCourseSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserWebinarSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.AllowAny]


class UserCourseViewSet(viewsets.ModelViewSet):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserWebinarViewSet(viewsets.ModelViewSet):
    queryset = UserWebinar.objects.all()
    serializer_class = UserWebinarSerializer
    permission_classes = [permissions.IsAuthenticated]
