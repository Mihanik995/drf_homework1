from rest_framework import test, status

from courses.models import Course
from users.models import User


class PaymentTestCase(test.APITestCase):
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

    def test_create_or_delete(self):
        response = self.client.post('/users/subscription/', {
            'course': self.course.pk
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'подписка добавлена'})

        response = self.client.post('/users/subscription/', {
            'course': self.course.pk
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'подписка удалена'})
