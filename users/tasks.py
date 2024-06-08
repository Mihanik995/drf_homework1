from datetime import datetime, timedelta

from celery import shared_task

from users.models import User


@shared_task
def check_user_activity():
    for user in User.objects.filter(is_active=True):
        if user.last_login:
            if user.last_login < datetime.now() - timedelta(days=30):
                user.is_active = False
                user.save()
