from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import NULLABLE, Lesson, Course


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    phone = models.IntegerField()
    city = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='users/', **NULLABLE)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Payment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    summ = models.PositiveIntegerField()
    payment_method = models.CharField(choices=(('cash', 'By cash'),
                                               ('transaction', 'Bank transaction'),
                                               )
                                      )

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    lesson = models.ForeignKey(to=Lesson, on_delete=models.SET_NULL, **NULLABLE)
    course = models.ForeignKey(to=Course, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.user}: {self.date} - {self.summ}"

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
