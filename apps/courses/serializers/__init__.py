# from .frontend_translation import FrontendTranslationSerializer
# from .version_history import VersionHistorySerializer

from .serializers import (
    CategorySerializer,
    CourseSerializer,
    WebinarSerializer,
    ModuleSerializer,
    LessonSerializer,
    CommentSerializer,
)

__all__ = [
    "FrontendTranslationSerializer",
    "VersionHistorySerializer",
    "CourseSerializer",
    "WebinarSerializer",
    "CategorySerializer",
    "ModuleSerializer",
    "LessonSerializer",
    "CommentSerializer"
]
