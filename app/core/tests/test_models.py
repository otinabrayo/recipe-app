''''Tests for models # noqa: E501'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


def create_user(email='test@examole.com', password='test'):
    return get_user_model().objects.create(email=email, password=password)


class ModelTests(TestCase):

    def test_create_user_with_email_success(self):
        email = "test@example.com"
        password = "password123"
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        data = [
            ['test1@example.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com']
        ]
        for email, expected in data:
            user = get_user_model().objects.create_user(email, "password123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "password123")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser('test@example.com', 'test123')   # noqa: E501

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user('test@example.com', 'test123')    # noqa
        recipe = models.Recipe.objects.create(
            user=user,
            title='Test Recipe',
            time_minutes=10,
            description="Test Recipe Description",
            price=Decimal('9.99')
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag 1')

        self.assertEqual(str(tag), tag.name)
