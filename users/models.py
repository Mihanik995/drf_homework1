from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    phone = models.IntegerField()
    city = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='users/', **NULLABLE)
