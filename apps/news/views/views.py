from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.news.models import (
    Post,
    Event,
    Survey,
    Question,
    QuestionOption,
    Submission
)
from apps.news.serializers import (
    PostSerializer,
    EventSerializer,
    SurveySerializer,
    QuestionSerializer,
    QuestionOptionSerializer,
    SubmissionSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Admin bo‘lmasa faqat o‘qishga ruxsat."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "description", "location_name"]
    filterset_fields = ["datetime", "location_name"]
    ordering_fields = ["datetime", "created_at"]


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all().prefetch_related("questions")
    serializer_class = SurveySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["title", "description"]
    filterset_fields = ["course"]
    ordering_fields = ["created_at"]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().prefetch_related("options")
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["survey"]


class QuestionOptionViewSet(viewsets.ModelViewSet):
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["question"]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all().select_related("user", "question", "chosen_option")
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["user", "question"]
    ordering_fields = ["created_at"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)