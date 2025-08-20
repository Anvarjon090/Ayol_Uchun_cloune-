from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="Anvarjon Uno API",
      default_version='v1',
      description="API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
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
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
