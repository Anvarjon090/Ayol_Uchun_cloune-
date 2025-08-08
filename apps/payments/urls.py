from django.urls import include, path

app_name = "payments"


urlpatterns = [
    path("paylov/", include("apps.payments.paylov.urls", namespace="paylov")),
]