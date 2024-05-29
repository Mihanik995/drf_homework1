from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserCreateAPIView, UserUpdateAPIView, UserDestroyAPIView, \
    UserRetrieveAPIView, SubscriptionAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),

    path('users/new/', UserCreateAPIView.as_view(), name='register'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='delete_user'),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/subscription/', SubscriptionAPIView.as_view(), name='subscription'),
]
