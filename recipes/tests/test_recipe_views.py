from django.urls import resolve, reverse

from .test_recipe_base import RecipeTestBase
from recipes import views


class RecipeViewsTest(RecipeTestBase):
    # Home:
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe(preparation_time=5)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertIn('5 Minutes', content)
        self.assertIn('Recipe Description', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_loads_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))

        self.assertIn('No recipes found', response.content.decode('utf-8'))

    # Category:
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        self.make_recipe(title='This is a Category Test')

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn('This is a Category Test', content)
        self.assertIn('10 Minutes', content)
        self.assertIn('Recipe Description', content)

    def test_recipe_category_template_dont_loads_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': recipe.category.id}))

        self.assertEqual(response.status_code, 404)

    # Recipe:
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 100}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_correct_recipes(self):
        self.make_recipe(title='This is a Detail Test')

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn('This is a Detail Test', content)

    def test_recipe_detail_template_dont_loads_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': recipe.category.id}))

        self.assertEqual(response.status_code, 404)