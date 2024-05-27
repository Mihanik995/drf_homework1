from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='courses/', **NULLABLE)

    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='lessons/', **NULLABLE)
    video_link = models.TextField(**NULLABLE)

    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return self.title
