from celery import shared_task
from django.core.mail import EmailMessage

from courses.models import Course


@shared_task
def send_update_notification(course, email):
    message = EmailMessage(
        f"{course} course was updated!",
        f'{course} course got some updates! Visit your personal cabinet to check them!',
        to=[email]
    )
    message.send()
