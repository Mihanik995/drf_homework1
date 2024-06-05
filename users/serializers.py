import stripe
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from config import settings
from courses.models import Course, Lesson
from users.models import Payment, User, Subscription

stripe.api_key = settings.STRIPE_API_KEY


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        if validated_data['course'] is None and validated_data['lesson'] is None:
            raise serializers.ValidationError('Payment should be associated with any course or lesson')

        payment = Payment.objects.create(
            payment_method=validated_data['payment_method'],
            user=validated_data['user']
        )
        if validated_data.__contains__('course'):
            payment.course = validated_data['course']
            stripe_price_id = payment.course.stripe_price_id

        else:
            payment.lesson = validated_data['lesson']
            stripe_price_id = payment.lesson.stripe_price_id
        stripe_price = stripe.Price.retrieve(stripe_price_id)
        payment.summ = stripe_price['unit_amount']

        if payment.payment_method in ['transaction']:
            checkout_session = stripe.checkout.Session.create(
                success_url="https://example.com/success",
                line_items=[{"price": stripe_price_id, "quantity": 1}],
                mode="payment",
                customer_email=payment.user.email
            )
            payment.payment_url = checkout_session.url

        payment.save()
        return payment



class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'phone', 'city')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone=validated_data['phone'],
            city=validated_data['city'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('course',)


class UserSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(source='subscription_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'phone', 'city', 'subscriptions',)
