# from .frontend_translation import FrontendTranslationSerializer
# from .version_history import VersionHistorySerializer

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    CourseSerializer,
    LessonSerializer,
    ModuleSerializer,
    WebinarSerializer,
)

__all__ = [
    "CategorySerializer",
    "CommentSerializer",
    "CourseSerializer",
    "FrontendTranslationSerializer",
    "LessonSerializer",
    "ModuleSerializer",
    "VersionHistorySerializer",
    "WebinarSerializer",
]
