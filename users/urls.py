from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import LoginAPIView, UserCreateAPIView, PurchasesCreateOrDeliteOrUpdateAPIView, PurchasesListAPIView, \
    delete_all_purchases

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='users_create'),
    path('token/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('purchases/', PurchasesCreateOrDeliteOrUpdateAPIView.as_view(), name='add/delite/update-purchases'),
    path('purchases-all/', PurchasesListAPIView.as_view(), name='purchases_all'),
    path('purchases-delete/', delete_all_purchases, name='purchases_delete')
]