from django.contrib.auth import get_user_model
from datetime import datetime
from django.test import TestCase

User = get_user_model()


class TestCategoryModel(TestCase):

    def test_create_category(self):
        category = User.objects.create(
            email='first@gmail.com', first_name='Alex', last_name='Gustavo',
            social_network='https://www.instagram.com/', phone_number='+996700000000',
            otp_code='456789', otp_code_expiry=datetime.now, is_verified=True,
            email_verified=True, phone_verified=True, balance=100
        )
        self.assertEqual(category.email, 'first@gmail.com')
        self.assertEqual(category.first_name, 'Alex'),
        self.assertEqual(category.last_name, 'Gustavo'),
        self.assertEqual(category.social_network, 'https://www.instagram.com/'),
        self.assertEqual(category.phone_number, '+996700000000'),
        self.assertEqual(category.otp_code, '456789'),
        self.assertEqual(category.otp_code_expiry, datetime.now),
        self.assertEqual(category.is_verified, True),
        self.assertEqual(category.email_verified, True),
        self.assertEqual(category.phone_verified, True),
        self.assertEqual(category.balance, 100),

