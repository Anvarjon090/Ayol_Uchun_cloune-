from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    CourseViewSet,
    LessonViewSet,
    ModuleViewSet,
    WebinarViewSet,
)

app_name = "courses"

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("courses", CourseViewSet)
router.register("webinars", WebinarViewSet)
router.register("modules", ModuleViewSet)
router.register("lessons", LessonViewSet)
router.register("comments", CommentViewSet)

urlpatterns = router.urls
