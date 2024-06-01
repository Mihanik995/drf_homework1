from rest_framework import serializers

from courses.models import Lesson, Course
from courses.validators import YoutubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YoutubeLinkValidator(field='video_link')]


class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'description',)


class CourseSerializer(serializers.ModelSerializer):
    lessons_amount = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(source='lesson_set', many=True, read_only=True)
    you_subscribed = serializers.SerializerMethodField()

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
