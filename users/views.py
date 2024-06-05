from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from users.models import Payment, User, Subscription
from users.permissions import IsOwnerOrStaff
from users.serializers import PaymentSerializer, UserRegisterSerializer, UserSerializer, SubscriptionSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('date',)
    filterset_fields = ('course', 'lesson', 'payment_method',)

class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrStaff]


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrStaff]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class SubscriptionAPIView(APIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @swagger_auto_schema(operation_id='user_subscription_create_or_delete',
                         request_body=SubscriptionSerializer,
                         responses={
                             200: 'подписка удалена / подписка добавлена',
                         })
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course = Course.objects.get(id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course)
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course).save()
            message = 'подписка добавлена'
        return Response({'message': message})
