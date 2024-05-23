from django.urls import path, include
from rest_framework import routers

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = CoursesConfig.name

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('lessons/new/', LessonCreateAPIView.as_view(), name='add_lesson'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='update_lesson'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='delete_lesson'),
] + router.urls
