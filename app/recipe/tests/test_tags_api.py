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
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        user = get_user_model().objects.create_user(
            'test@example.com',
            'password123'
        )
        self.client.force_authenticate(user=user)

        # Create tags with the user
        Tag.objects.create(user=user, name='Dessert')

        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)


    def test_tags_limited_user(self):
        user2 = create_user(email='test2@example.com')
        Tag.objects.create(name='Vegan', user=user2)
        tag = Tag.objects.create(user=self.user, name='test')

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)
        self.assertEqual(response.data[0]['id'], tag.id)
