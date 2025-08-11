from django.urls import include, path

from apps.payments.views import OrderCreateAPIView, AddUserCardAPIView, ConfirmUserCardAPIView

app_name = "payments"


urlpatterns = [
    path("order/create/", OrderCreateAPIView.as_view(), name="create-order"),
    path("usercard/add/", AddUserCardAPIView.as_view(), name="add-usercard"),
    path("usercard/confirm/", ConfirmUserCardAPIView.as_view(), name="confirm-usercard"),
    # Payment Provider callbacks
    path("paylov/", include("apps.payments.paylov.urls", namespace="paylov")),
]