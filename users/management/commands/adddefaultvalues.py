from datetime import datetime

from django.core.management import BaseCommand

from courses.models import Lesson, Course
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        default_course = Course.objects.create(
            title='default course',
            description='default course description'
        )
        default_course.save()

        default_lesson = Lesson.objects.create(
            title='default lesson',
            description='default lesson description',
            course=default_course
        )
        default_lesson.save()

        Payment.objects.create(
            summ=1000,
            user=User.objects.get(email='admin@test.com'),
            payment_method='cash',
            lesson=default_lesson
        ).save()
        Payment.objects.create(
            summ=10000,
            user=User.objects.get(email='admin@test.com'),
            payment_method='transaction',
            course=default_course
        ).save()
