# from .frontend_translations import FrontendTranslationView
# from .version_history import VersionHistoryView

from rest_framework import viewsets

from .views import (
    CategoryViewSet,
    CommentViewSet,
    CourseViewSet,
    LessonViewSet,
    ModuleViewSet,
    WebinarViewSet,
)

__all__ = [
    "CategoryView",
    "CommentView",
    "CourseView",
    "FrontendTranslationView",
    "LessonView",
    "ModuleView",
    "VersionHistoryView",
    "WebinarView",
]
