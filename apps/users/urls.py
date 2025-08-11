from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.users.views.views import RegisterView
from apps.users.views import (
    UserViewSet, 
    InterestViewSet,
    UserCourseViewSet, 
    UserWebinarViewSet,
)


app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"interests", InterestViewSet)
router.register(r"user-courses", UserCourseViewSet)
router.register(r"user-webinars", UserWebinarViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
]

urlpatterns += router.urls