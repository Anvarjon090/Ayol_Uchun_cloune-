from django.urls import path

from apps.common.views import FrontendTranslationView, VersionHistoryView

app_name = "common"

urlpatterns = [
    path(
        "FrontendTranslations/",
        FrontendTranslationView.as_view(),
        name="frontend-translations",
    ),
    path("VersionHistory/", VersionHistoryView.as_view(), name="version-history"),
]
