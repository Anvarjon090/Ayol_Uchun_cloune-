# from .frontend_translations import FrontendTranslationView
# from .version_history import VersionHistoryView

# __all__ = [
#     "FrontendTranslationView",
#     "VersionHistoryView",
# ]

from rest_framework import viewsets

from .views import (
    EventViewSet,
    PostViewSet,
    QuestionOptionViewSet,
    QuestionViewSet,
    SubmissionViewSet,
    SurveyViewSet,
)
