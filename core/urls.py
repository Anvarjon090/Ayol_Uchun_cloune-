from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .schema import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/common/", include("apps.common.urls", namespace="common")),
    path("api/v1/payments/", include("apps.payments.urls", namespace="payments")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/courses/", include("apps.courses.urls", namespace="courses")),
    path("api/news/", include("apps.news.urls", namespace="news")),
    path("api/users/", include("apps.users.urls", namespace="users")),
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
