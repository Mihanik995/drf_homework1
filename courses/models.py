from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='courses/')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='lessons/')
    video_link = models.TextField()

    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
