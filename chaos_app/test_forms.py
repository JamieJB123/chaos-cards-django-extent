from django.test import TestCase
from django.contrib.auth.models import User
from chaos_app.forms import CardForm
from chaos_app.models import Card


class CardFormTest(TestCase):
    """Test cases for the CardForm"""

    def setUp(self):
        """Set up test data"""
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_card_form_valid_data(self):
        """Test that form is valid with correct data"""
        form_data = {
            'title': 'Test Card',
            'content': 'This is a test card.',
            'featured_image': None  # No image provided
        }
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())
        card = form.save(commit=False)
        card.user = self.user
        card.save()
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Card.objects.first().title, 'Test Card')

    def test_card_form_empty_title(self):
        """Test that form is invalid with empty title"""
        form_data = {
            'title': '',
            'content': 'This is a test card.',
            'featured_image': None  # No image provided
        }
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_card_form_empty_content(self):
        """Test that form is invalid with empty content"""
        form_data = {
            'title': 'Test Card',
            'content': '',
            'featured_image': None  # No image provided
        }
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_card_form_title_max_length(self):
        """Test that form respects title max_length constraint"""
        form_data = {
            'title': 'x' * 201,
            'content': 'This is a test card.',
            'featured_image': None  # No image provided
        }
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_card_form_content_max_length(self):
        """Test that form respects content max_length constraint"""
        form_data = {
            'title': 'Test Card',
            'content': 'x' * 501,
            'featured_image': None  # No image provided
        }
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_card_form_without_image(self):
        """Test that form is valid without featured_image"""
        form_data = {
            'title': 'Test Card',
            'content': 'This is a test card.',
            'featured_image': None  # No image provided
        }
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_card_form_fields_included(self):
        """Test that form includes correct fields"""
        form = CardForm()
        self.assertIn('title', form.fields)
        self.assertIn('content', form.fields)
        self.assertIn('featured_image', form.fields)

