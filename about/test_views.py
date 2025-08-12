from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from about.models import About, CollaborateRequest
from about.forms import FeedbackForm


class AboutViewTest(TestCase):
    """Test cases for the about view"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.url = reverse('about')
        self.about = About.objects.create(author=self.user, content='First about', updated_on='2024-06-01')
        self.valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'I want to collaborate!'
        }
        self.invalid_data = {
            'name': '',
            'email': 'not-an-email',
            'message': ''
        }

    def test_about_view_get_request(self):
        """Test GET request to about view"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_about_view_template_used(self):
        """Test correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'about/about.html')

    def test_about_view_context_data(self):
        """Test context data passed to template"""
        response = self.client.get(self.url)
        self.assertIn('about', response.context)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], FeedbackForm)

    def test_about_view_post_valid_form(self):
        """Test POST request with valid feedback form data"""
        response = self.client.post(self.url, self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CollaborateRequest.objects.filter(email='john@example.com').exists())

    def test_about_view_post_invalid_form(self):
        """Test POST request with invalid feedback form data"""
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, 200)

        # Check that the form is in the context and isn't valid
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertFalse(form.is_valid())

        self.assertContains(response, 'Error sending contact form. Please try again.')

    def test_about_view_success_message(self):
        """Test success message on valid form submission"""
        response = self.client.post(self.url, self.valid_data, follow=True)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Contact form sent successfully!', messages)

    def test_about_view_redirect_after_post(self):
        """Test redirect after successful form submission"""
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)
