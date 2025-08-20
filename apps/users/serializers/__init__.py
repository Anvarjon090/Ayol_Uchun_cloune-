# from .frontend_translation import FrontendTranslationSerializer
# from .version_history import VersionHistorySerializer

# __all__ = [
#     "FrontendTranslationSerializer",
#     "VersionHistorySerializer",
# ]
from rest_framework import serializers

from .serializers import (
    InterestSerializer,
    UserCourseSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserWebinarSerializer,
)
