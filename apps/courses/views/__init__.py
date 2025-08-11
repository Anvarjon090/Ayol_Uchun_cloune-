# from .frontend_translations import FrontendTranslationView
# from .version_history import VersionHistoryView

from rest_framework import viewsets
from .views import (
    CategoryViewSet,
    CourseViewSet,
    WebinarViewSet,
    ModuleViewSet,
    LessonViewSet,
    CommentViewSet,
)


__all__ = [
    "FrontendTranslationView",
    "VersionHistoryView",
    "CourseView",
    "WebinarView",
    "CategoryView",
    "ModuleView",
    "LessonView",
    "CommentView"
]
