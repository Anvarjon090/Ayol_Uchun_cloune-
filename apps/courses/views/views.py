from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg


from apps.courses.models import Course, Webinar, Category, Module, Lesson, Comment
from apps.courses.serializers import (
    CourseSerializer,
    WebinarSerializer,
    CategorySerializer,
    ModuleSerializer,
    LessonSerializer,
    CommentSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related("category", "author").prefetch_related("modules")
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "author", "price"]
    search_fields = ["title", "description"]
    ordering_fields = ["price", "rating", "created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        # annotate average rating from comments if you want to show it
        qs = qs.annotate(average_rating=Avg("comments__rating"))
        return qs

    def perform_create(self, serializer):
        # author will be request.user
        serializer.save(author=self.request.user)


class WebinarViewSet(viewsets.ModelViewSet):
    queryset = Webinar.objects.all().select_related("category", "author")
    serializer_class = WebinarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "author", "datetime"]
    search_fields = ["title", "description"]
    ordering_fields = ["datetime", "price", "rating"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all().select_related("course")
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().select_related("module")
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("user", "course", "webinar")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["user", "course", "webinar", "rating"]
    search_fields = ["text"]
    ordering_fields = ["rating", "created_at"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)