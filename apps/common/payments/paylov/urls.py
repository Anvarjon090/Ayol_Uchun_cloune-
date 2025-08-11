from django.urls import path

from apps.payments.paylov.views import PaylovAPIView

app_name = "paylov"

urlpatterns = [
    path("callback/", PaylovAPIView.as_view(), name="paylov-callback"),
]