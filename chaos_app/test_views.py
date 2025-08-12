from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from chaos_app.models import Card
from chaos_app.forms import CardForm


class HomeViewTest(TestCase):
    """Test cases for the home view"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_home_view_authenticated_user(self):
        """Test home view for authenticated users"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chaos_app/home.html')
        self.assertContains(response, "Invitation unknown")

    def test_home_view_unauthenticated_user(self):
        """Test home view for unauthenticated users"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chaos_app/home.html')
        self.assertContains(response, "Welcome to |")

    def test_home_view_context_data(self):
        """Test context data passed to template"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['spin_attempted'], False)


class RandomCardViewTest(TestCase):
    """Test cases for the random_card_view"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_random_card_view_requires_login(self):
        """Test that view requires user authentication"""
        self.client.logout()
        response = self.client.get(reverse('spin_card'))
        # Use the correct login URL from your allauth setup
        self.assertRedirects(response, f"/accounts/login/?next={reverse('spin_card')}")

    def test_random_card_view_with_cards(self):
        """Test view when user has cards"""
        card = Card.objects.create(
            user=self.user,
            title="Test Card Title",  # Add the missing title
            content="Test Card Content"
        )
        response = self.client.get(reverse('spin_card'))
        self.assertEqual(response.context['random_card'], card)

    def test_random_card_view_without_cards(self):
        """Test view when user has no cards"""
        response = self.client.get(reverse('spin_card'))
        self.assertIsNone(response.context['random_card'])

    def test_random_card_view_spin_attempted_flag(self):
        """Test that spin_attempted flag is set"""
        response = self.client.get(reverse('spin_card'))
        self.assertTrue(response.context['spin_attempted'])

    def test_correct_template_used(self):
        """Test correct template is used"""
        response = self.client.get(reverse('spin_card'))
        self.assertTemplateUsed(response, 'chaos_app/home.html')

class UserCardsViewTest(TestCase):
    """Test cases for the user_cards_view"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_user_cards_view_requires_login(self):
        """Test that view requires user authentication"""
        self.client.logout()
        response = self.client.get(reverse('user_cards'))
        self.assertRedirects(response, f"/accounts/login/?next={reverse('user_cards')}")

    def test_user_cards_view_get_request(self):
        """Test GET request to user cards view"""
        response = self.client.get(reverse('user_cards'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chaos_app/user_cards.html')
        self.assertContains(response, "My Cards")

    def test_user_cards_view_post_valid_form(self):
        """Test POST request with valid form data"""
        response = self.client.post(reverse('user_cards'), {
            'title': 'Test Card',
            'content': 'Test Content'
        })
        self.assertRedirects(response, reverse('user_cards'))
        self.assertTrue(Card.objects.filter(title='Test Card').exists())

    def test_user_cards_view_post_invalid_form(self):
        """Test POST request with invalid form data"""
        response = self.client.post(reverse('user_cards'), {
            'title': '',
            'content': 'Test Content'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chaos_app/user_cards.html')
        self.assertContains(response, "This field is required.")


    def test_user_cards_view_only_user_cards(self):
        """Test that only user's own cards are displayed"""
        # Create a card for another user
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        Card.objects.create(
            user=other_user,
            title="Other User Card 55",
            content="Test Content"
        )
        Card.objects.create(
            user=self.user,  # Create a card for the logged-in user
            title = "User Card 123",
            content = "Test Content"
        )
        response = self.client.get(reverse('user_cards'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chaos_app/user_cards.html')
        self.assertContains(response, "User Card 123")
        self.assertNotContains(response, "Other User Card 55")

    def test_user_cards_view_success_message(self):
        """Test success message on card creation"""
        response = self.client.post(reverse('user_cards'), {
            'title': 'New Card',
            'content': 'Test Content'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_cards'))

        # Get messages from the response
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Card created successfully!")


    def test_user_cards_view_error_message(self):
        """Test error message on form validation failure"""
        response = self.client.post(reverse('user_cards'), {
            'title': '',
            'content': 'Test Content'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chaos_app/user_cards.html')
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Error creating card. Please try again.")


class EditCardViewTest(TestCase):
    """Test cases for the edit_card_view"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.card = Card.objects.create(
            user=self.user,
            title="Test Card",
            content="Test Content"
        )

    def test_edit_card_view_requires_login(self):
        """Test that view requires user authentication"""
        self.client.logout()
        response = self.client.get(reverse('edit_card', args=[self.card.id]))
        expected_next = reverse('edit_card', args=[self.card.id])
        self.assertRedirects(response, f"/accounts/login/?next={expected_next}")

    def test_edit_card_view_valid_form(self):
        """Test editing card with valid form data"""
        response = self.client.post(reverse('edit_card', args=[self.card.id]), {
            'title': 'Updated Title',
            'content': 'Updated Content'
        })
        self.assertRedirects(response, reverse('user_cards'))
        self.card.refresh_from_db()
        self.assertEqual(self.card.title, 'Updated Title')
        self.assertEqual(self.card.content, 'Updated Content')

    def test_edit_card_view_invalid_form(self):
        """Test editing card with invalid form data"""
        original_title = self.card.title
        original_content = self.card.content

        response = self.client.post(reverse('edit_card', args=[self.card.id]), {
            'title': '',  # Invalid - empty title
            'content': 'Updated Content'  # Valid content
        })

        # Should redirect to user_cards regardless (based on your view logic)
        self.assertRedirects(response, reverse('user_cards'))

        # Refresh card from database
        self.card.refresh_from_db()

        # Card should NOT be updated due to invalid form
        self.assertEqual(self.card.title, original_title)  # Title unchanged
        self.assertEqual(self.card.content, original_content)  # Content unchanged

        # Check that error message was set
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Error updating card. Please try again.")

    def test_edit_card_view_user_owns_card(self):
        """Test that user can only edit their own cards"""
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        other_card = Card.objects.create(
            user=other_user,
            title="Other User's Card",
            content="Other User's Content"
        )
        response = self.client.get(reverse('edit_card', args=[other_card.id]))
        self.assertEqual(response.status_code, 404)

    def test_edit_card_view_card_not_found(self):
        """Test behavior when card doesn't exist"""
        response = self.client.get(reverse('edit_card', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_edit_card_view_success_message(self):
        """Test success message on card update"""
        response = self.client.post(reverse('edit_card', args=[self.card.id]), {
            'title': 'Updated Title',
            'content': 'Updated Content'
        })
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Card updated successfully!")

    def test_edit_card_view_error_message(self):
        """Test error message on form validation failure"""
        response = self.client.post(reverse('edit_card', args=[self.card.id]), {
            'title': '',
            'content': 'Updated Content'
        })
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Error updating card. Please try again.")


    def test_edit_card_view_redirect(self):
        """Test redirect after successful edit"""
        response = self.client.post(reverse('edit_card', args=[self.card.id]), {
            'title': 'Updated Title',
            'content': 'Updated Content'
        })
        self.assertRedirects(response, reverse('user_cards'))


class DeleteCardViewTest(TestCase):
    """Test cases for the delete_card_view"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.card = Card.objects.create(
            user=self.user,
            title="Test Card",
            content="Test Content"
        )

    def test_delete_card_view_requires_login(self):
        """Test that view requires user authentication"""
        response = self.client.delete(reverse('delete-card', args=[self.card.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next=/my-cards/delete-card/{self.card.id}/")

    def test_delete_card_view_successful_deletion(self):
        """Test successful card deletion"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse('delete-card', args=[self.card.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_cards'))
        self.assertFalse(Card.objects.filter(id=self.card.id).exists())

    def test_delete_card_view_user_owns_card(self):
        """Test that user can only delete their own cards"""
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        other_card = Card.objects.create(
            user=other_user,
            title="Other User's Card",
            content="Other User's Content"
        )

        # LOGIN as the test user before making the request
        self.client.login(username='testuser', password='testpass')

        response = self.client.delete(reverse('delete-card', args=[other_card.id]))
        self.assertEqual(response.status_code, 404)

    def test_delete_card_view_card_not_found(self):
        """Test behavior when card doesn't exist"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse('delete-card', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_delete_card_view_success_message(self):
        """Test success message on card deletion"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse('delete-card', args=[self.card.id]))
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Card deleted successfully!")

    def test_delete_card_view_error_message(self):
        """Test error message when deletion fails"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse('delete-card', args=[999]))

        # 404 responses don't execute message logic
        self.assertEqual(response.status_code, 404)

        # No messages should be present since 404 bypasses view logic
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 0)

    def test_delete_card_view_redirect(self):
        """Test redirect after deletion"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse('delete-card', args=[self.card.id]))
        self.assertRedirects(response, reverse('user_cards'))
