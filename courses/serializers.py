from rest_framework import serializers

from courses.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_amount = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True)
    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_amount(self, instance):
        if instance.lesson_set:
            return instance.lesson_set.count()
        return 0
