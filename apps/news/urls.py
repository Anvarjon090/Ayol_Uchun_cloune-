from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    EventViewSet,
    SurveyViewSet,
    QuestionViewSet,
    QuestionOptionViewSet,
    SubmissionViewSet,
)

app_name = "news"

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("events", EventViewSet)
router.register("surveys", SurveyViewSet)
router.register("questions", QuestionViewSet)
router.register("question-options", QuestionOptionViewSet)
router.register("submissions", SubmissionViewSet)

urlpatterns = router.urls