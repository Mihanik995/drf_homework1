import stripe
from rest_framework import serializers

from config import settings
from courses.models import Lesson, Course
from courses.tasks import send_update_notification
from courses.validators import YoutubeLinkValidator

stripe.api_key = settings.STRIPE_API_KEY


class LessonSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(write_only=True, default=0)

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YoutubeLinkValidator(field='video_link')]

    def create(self, validated_data):
        # product = stripe.Product.create(
        #     name=f'course "{validated_data['title']}"'
        # )
        #
        # price = stripe.Price.create(
        #     currency='usd',
        #     unit_amount=validated_data['price'] * 100,
        #     product_data={"name": f'course "{validated_data['title']}"'},
        # )
        #
        owner = self.context.get('request').user

        new_lesson = Lesson.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            image=validated_data['image'] if hasattr(validated_data, 'image') else None,
            video_link=validated_data['video_link'] if hasattr(validated_data, 'video_link') else None,
            course=validated_data['course'],

            owner=owner,
            # stripe_product_id=product.id,
            # stripe_price_id=price.id
        )

        subscribed_clients = [subscription.user for subscription in new_lesson.course.subscription_set.all()]
        course_title = new_lesson.course.title

        for client in subscribed_clients:
            send_update_notification.delay(course=course_title, email=client.email)

        return new_lesson


class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'description',)


class CourseSerializer(serializers.ModelSerializer):
    lessons_amount = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(source='lesson_set', many=True, read_only=True)
    you_subscribed = serializers.SerializerMethodField()

    price = serializers.IntegerField(write_only=True, default=0)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_amount(self, instance):
        if instance.lesson_set:
            return instance.lesson_set.count()
        return 0

    def get_you_subscribed(self, instance):
        course_subscribers = [subscription.user for subscription in instance.subscription_set.all()]

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return user in course_subscribers

    def create(self, validated_data):
        product = stripe.Product.create(
            name=f'course "{validated_data['title']}"'
        )

        price = stripe.Price.create(
            currency='usd',
            unit_amount=validated_data['price']*100,
            product_data={"name": f'course "{validated_data['title']}"'},
        )

        owner = self.context.get('request').user

        new_course = Course.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            preview=validated_data['preview'] if hasattr(validated_data, 'preview') else None,

            owner=owner,
            stripe_product_id=product.id,
            stripe_price_id=price.id
        )

        return new_course
