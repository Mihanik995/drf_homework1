from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        default_moderator = User.objects.create(
            email='defaultmoderator@test.com',
            phone=112,
            city='Blablatown',
        )
        default_moderator.set_password('1234567890aA')
        default_moderator.save()

        my_group = Group.objects.get(name='Moderators')
        my_group.user_set.add(default_moderator)
