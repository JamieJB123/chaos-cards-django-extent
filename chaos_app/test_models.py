from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from chaos_app.models import Card


class CardModelTest(TestCase):
    """Test cases for the Card model"""

    def setUp(self):
        """Set up test data"""
        # Create test user and card instances
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.card = Card.objects.create(
            title='Test Card',
            content='This is a test card.',
            user=self.user
        )

    def test_card_creation(self):
        """Test that a card can be created with valid data"""
        # Test card creation with all required fields
        self.assertEqual(self.card.title, 'Test Card')
        self.assertEqual(self.card.content, 'This is a test card.')
        self.assertEqual(self.card.user, self.user)

    def test_card_string_representation(self):
        """Test the string representation of the card"""
        self.assertEqual(str(self.card), 'Test Card by testuser')

    def test_card_user_relationship(self):
        """Test the foreign key relationship with User"""
        self.assertEqual(self.card.user.username, 'testuser')

    def test_card_title_max_length(self):
        """Test that card title respects max_length constraint"""
        # Test title field max_length of 200 characters
        self.card.title = 'x' * 201
        with self.assertRaises(ValidationError):
            self.card.full_clean()

    def test_card_content_max_length(self):
        """Test that card content respects max_length constraint"""
        # Test content field max_length of 500 characters
        self.card.content = 'x' * 501
        with self.assertRaises(ValidationError):
            self.card.full_clean()

    def test_card_default_featured_image(self):
        """Test that card has default placeholder image"""
        # Test default value for featured_image field
        self.assertEqual(self.card.featured_image, 'placeholder')

    def test_card_created_on_auto_set(self):
        """Test that created_on is automatically set"""
        # Test that created_on field is auto-populated
        self.assertIsNotNone(self.card.created_on)

    def test_card_ordering(self):
        """Test that cards are ordered by created_on descending"""
        # Test the Meta ordering configuration
        self.assertEqual(Card._meta.ordering, ['-created_on'])

    def test_card_meta_verbose_names(self):
        """Test the verbose name and verbose name plural"""
        self.assertEqual(Card._meta.verbose_name, 'Card')
        self.assertEqual(Card._meta.verbose_name_plural, 'Cards')

    def test_card_cascade_delete(self):
        """Test that cards are deleted when user is deleted"""
        # Test CASCADE behavior on user deletion
        self.user.delete()
        self.assertEqual(Card.objects.count(), 0)

    def test_card_related_name(self):
        """Test the related_name 'cards' works correctly"""
        # Test that user.cards returns user's cards
        self.assertEqual(self.user.cards.count(), 1)
        self.assertEqual(self.user.cards.first(), self.card)

# Edge Case Tests

    def test_card_empty_title(self):
        """Test that card cannot be created with empty title"""
        card = Card(user=self.user, title='', content='This is a test card.')
        with self.assertRaises(ValidationError):
            card.full_clean()

    def test_card_empty_content(self):
        """Test that card cannot be created with empty content"""
        card = Card(user=self.user, title='Test Card', content='')
        with self.assertRaises(ValidationError):
            card.full_clean()


