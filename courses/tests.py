from rest_framework import test, status

from courses.models import Course, Lesson
from users.models import User


class LessonsTestCase(test.APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='dafeault@email.com',
            phone=111,
            city='Default'
        )
        self.user.set_password('qwe123rty456')

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Default course',
            description='Default course description'
        )

        self.lesson = Lesson.objects.create(
            title='Default lesson',
            description='Default lesson description',
            course=self.course
        )

        # response = self.client.post('/courses/', data={
        #     "title": "Default course'",
        #     "description": 'Default course description'
        # })
        # self.course_id = response.json()['id']
        #
        # response = self.client.post('/lessons/new/', data={
        #     "title": "Default course'",
        #     "description": 'Default course description',
        #     'course': self.course_id
        # })
        # self.lesson_id = response.json()['id']

    def test_list(self):
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):
        response = self.client.get(f'/lessons/{self.lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        response = self.client.post('/lessons/new/', {
            'title': 'New default lesson',
            'description': 'New default lesson description',
            'course': self.course.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        response = self.client.put(f'/lessons/{self.lesson.pk}/update/', {
            'title': 'Default lesson',
            'description': 'New default lesson description',
            'course': self.course.pk
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], 'New default lesson description')

    def test_patch(self):
        response = self.client.patch(f'/lessons/{self.lesson.pk}/update/', {
            'description': 'New default lesson description'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], 'New default lesson description')

    def test_delete(self):
        response = self.client.delete(f'/lessons/{self.lesson.pk}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
