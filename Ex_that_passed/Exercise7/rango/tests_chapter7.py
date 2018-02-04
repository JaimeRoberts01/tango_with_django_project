# Chapter 3
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
import os

#Chapter 4
from django.contrib.staticfiles import finders

#Chapter 5
from rango.models import Page, Category
import populate_rango
import rango.test_utils as test_utils

#Chapter 6
from rango.decorators import chapter6

#Chapter 7
from rango.decorators import chapter7
from rango.forms import CategoryForm, PageForm

# ===== Chapter 7
class Chapter7ViewTests(TestCase):
    @chapter7
    def test_index_contains_link_to_add_category(self):
        # Access index
        try:
            response = self.client.get(reverse('index'))
        except:
            try:
                response = self.client.get(reverse('rango:index'))
            except:
                return False

        # Check if there is text and a link to add category
        self.assertIn('href="' + reverse('add_category') + '"', response.content.decode('ascii'))

    @chapter7
    def test_add_category_form_is_displayed_correctly(self):
        # Access add category page
        response = self.client.get(reverse('add_category'))

        # Check form in response context is instance of CategoryForm
        self.assertTrue(isinstance(response.context['form'], CategoryForm))

        # Check form is displayed correctly
        # Header
        self.assertIn('<h1>Add a Category</h1>'.lower(), response.content.decode('ascii').lower())

        # Label
        self.assertIn('Please enter the category name.'.lower(), response.content.decode('ascii').lower())

        # Text input
        self.assertIn('id="id_name"', response.content.decode('ascii'))
        self.assertIn('maxlength="128"', response.content.decode('ascii'))
        self.assertIn('name="name"', response.content.decode('ascii'))
        self.assertIn('type="text"', response.content.decode('ascii'))

        # Button
        self.assertIn('type="submit" name="submit" value="Create Category"'.lower(), response.content.decode('ascii').lower())

    @chapter7
    def test_add_page_form_is_displayed_correctly(self):
        # Create categories
        categories = test_utils.create_categories()

        for category in categories:
            # Access add category page
            try:
                response = self.client.get(reverse('index'))
                response = self.client.get(reverse('add_page', args=[category.slug]))
            except:
                try:
                    response = self.client.get(reverse('rango:index'))
                    response = self.client.get(reverse('rango:add_page', args=[category.slug]))
                except:
                    return False

            # Check form in response context is instance of CategoryForm
            self.assertTrue(isinstance(response.context['form'], PageForm))

            # Check form is displayed correctly

            # Label 1
            self.assertIn('Please enter the title of the page.'.lower(), response.content.decode('ascii').lower())

            # Label 2
            self.assertIn('Please enter the URL of the page.'.lower(), response.content.decode('ascii').lower())

            # Text input 1
            self.assertIn('id="id_title"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('maxlength="128"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('name="title"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('type="text"'.lower(), response.content.decode('ascii').lower())

            # Text input 2
            self.assertIn('id="id_url"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('maxlength="200"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('name="url"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('type="url"'.lower(), response.content.decode('ascii').lower())

            # Button
            self.assertIn('type="submit" name="submit" value="Add Page"'.lower(), response.content.decode('ascii').lower())

    def test_access_category_that_does_not_exists(self):
        # Access a category that does not exist
        response = self.client.get(reverse('show_category', args=['python']))

        # Check that it has a response as status code OK is 200
        self.assertEquals(response.status_code, 200)

        # Check the rendered page is not empty, thus it was customised (I suppose)
        self.assertNotEquals(response.content.decode('ascii'), '')

    def test_link_to_add_page_only_appears_in_valid_categories(self):
        # Access a category that does not exist
        response = self.client.get(reverse('show_category', args=['python']))

        # Check that there is not a link to add page
        try:
            self.assertNotIn(reverse('add_page', args=['python']), response.content.decode('ascii'))
            # Access a category that does not exist
            response = self.client.get(reverse('show_category', args=['other-frameworks']))
            # Check that there is not a link to add page
            self.assertNotIn(reverse('add_page', args=['other-frameworks']), response.content.decode('ascii'))
        except:
            try:
                self.assertNotIn(reverse('rango:add_page', args=['python']), response.content.decode('ascii'))
                # Access a category that does not exist
                response = self.client.get(reverse('rango:show_category', args=['other-frameworks']))
                # Check that there is not a link to add page
                self.assertNotIn(reverse('rango:add_page', args=['other-frameworks']), response.content.decode('ascii'))
            except:
                return False

    @chapter7
    def test_category_contains_link_to_add_page(self):
        # Crete categories
        categories = test_utils.create_categories()

        # For each category in the database check if contains link to add page
        for category in categories:
            try:
                response = self.client.get(reverse('show_category', args=[category.slug]))
                self.assertIn(reverse('add_page', args=[category.slug]), response.content.decode('ascii'))
            except:
                try:
                    response = self.client.get(reverse('rango:show_category', args=[category.slug]))
                    self.assertIn(reverse('rango:add_page', args=[category.slug]), response.content.decode('ascii'))
                except:
                    return False
