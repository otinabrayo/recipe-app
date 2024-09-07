from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def create_user(email='test@example.com', password='test'):
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
    def test_auth_required(self):
        
