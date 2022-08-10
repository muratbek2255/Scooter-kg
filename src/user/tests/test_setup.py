from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker

User = get_user_model()


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('auth_register')
        self.login_url = reverse('auth_login')
        self.fake = Faker()

        self.user_data = {
            'email': self.fake.email(),
            'username': self.fake.email().split('@')[0],
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'phone_number': self.fake.phone_number(),
            'password': self.fake.password(),
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
