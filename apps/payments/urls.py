from django.urls import include, path

from apps.payments.views import (
    AddUserCardAPIView,
    ConfirmUserCardAPIView,
    DeleteUserCardAPIView,
    GetSingleUserCardAPIView,
    ListUserCardsAPIView,
    OrderCreateAPIView,
    UserCardReceiptCreateAPIView,
    UserCardReceiptConfirmAPIView,
)

app_name = "payments"


urlpatterns = [
    path("order/create/", OrderCreateAPIView.as_view(), name="create-order"),
    path("usercard/add/", AddUserCardAPIView.as_view(), name="add-usercard"),
    path(
        "usercard/confirm/", ConfirmUserCardAPIView.as_view(), name="confirm-usercard"
    ),
    path(
        "usercard/<int:user_id>/list/",
        ListUserCardsAPIView.as_view(),
        name="list-usercards",
    ),
    path("usercard/delete/", DeleteUserCardAPIView.as_view(), name="delete-usercard"),
    path(
        "usercard/<str:card_id>/single/",
        GetSingleUserCardAPIView.as_view(),
        name="single-usercard",
    ),
    path(
        "usercard/receipt/create/", UserCardReceiptCreateAPIView.as_view(), name="create-receipt"
    ),
    path("usercard/receipt/pay/", UserCardReceiptConfirmAPIView.as_view(), name="pay-receipt"),
    # Payment Provider callbacks
    path("paylov/", include("apps.payments.paylov.urls", namespace="paylov")),
]