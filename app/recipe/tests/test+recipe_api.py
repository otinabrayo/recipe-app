from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from decimal import Decimal
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):

    defaults = {
        'title': 'Test Recipe',
        'time_minutes': 10,
        'price': Decimal('10.00'),
        'description': 'Test Recipe Description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.GET(RECIPE_URL)
        self.assertEqual(response.status_code, 401)


class PrivateRecipeApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'test123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        response = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('_id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_recipe_list_to_user(self):
        other_user = get_user_model().objects.create_user('other@example.com', 'password123')     # noqa
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        response = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_get_recipe_detail(self):
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.user)
        response = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(response.data, serializer.data)
