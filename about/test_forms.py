from django.test import TestCase
from about.forms import FeedbackForm
from about.models import CollaborateRequest


class FeedbackFormTest(TestCase):
    """Test cases for the FeedbackForm"""

    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'This is a feedback message.'
        }

    def test_feedback_form_valid_data(self):
        """Test that form is valid with correct data"""
        form = FeedbackForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_empty_name(self):
        """Test that form is invalid with empty name"""
        data = self.valid_data.copy()
        data['name'] = ''
        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_feedback_form_empty_email(self):
        """Test that form is invalid with empty email"""
        data = self.valid_data.copy()
        data['email'] = ''
        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_feedback_form_empty_message(self):
        """Test that form is invalid with empty message"""
        data = self.valid_data.copy()
        data['message'] = ''
        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_feedback_form_name_max_length(self):
        """Test that form respects name max_length constraint"""
        data = self.valid_data.copy()
        data['name'] = 'a' * 201
        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_feedback_form_email_max_length(self):
        """Test that form respects email max_length constraint"""
        data = self.valid_data.copy()
        data['email'] = 'a' * 255 + '@example.com'
        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_feedback_form_message_max_length(self):
        """Test that form respects message max_length constraint"""
        data = self.valid_data.copy()
        data['message'] = 'a' * 501
        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_feedback_form_invalid_email_format(self):
        """Test that form validates email format"""
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_feedback_form_save_method(self):
        """Test that form saves correctly"""
        form = FeedbackForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertIsInstance(instance, CollaborateRequest)
        self.assertEqual(instance.name, self.valid_data['name'])
        self.assertEqual(instance.email, self.valid_data['email'])
        self.assertEqual(instance.message, self.valid_data['message'])

    def test_feedback_form_fields_included(self):
        """Test that form includes correct fields"""
        form = FeedbackForm()
        expected_fields = ['name', 'email', 'message']
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_feedback_form_default_read_status(self):
        """Test that saved form creates request with default read status"""
        form = FeedbackForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertFalse(instance.read)

    def test_feedback_form_blank_fields(self):
        """Test form is invalid if all fields are blank"""
        form = FeedbackForm(data={'name': '', 'email': '', 'message': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('message', form.errors)

    def test_feedback_form_whitespace_name(self):
        """Test form is invalid if name is only whitespace"""
        data = self.valid_data.copy()
        data['name'] = '   '
        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_feedback_form_whitespace_message(self):
        """Test form is invalid if message is only whitespace"""
        data = self.valid_data.copy()
        data['message'] = '   '
        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_feedback_form_multiple_invalid_emails(self):
        """Test form is invalid for several bad email formats"""
        invalid_emails = ['plainaddress', 'missing@domain', 'missing.domain@', '@missingusername.com']
        for email in invalid_emails:
            data = self.valid_data.copy()
            data['email'] = email
            form = FeedbackForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn('email', form.errors)

    def test_feedback_form_unicode_name(self):
        """Test form accepts unicode characters in name"""
        data = self.valid_data.copy()
        data['name'] = 'José María'
        form = FeedbackForm(data=data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_unicode_message(self):
        """Test form accepts unicode characters in message"""
        data = self.valid_data.copy()
        data['message'] = 'こんにちは世界'
        form = FeedbackForm(data=data)
        self.assertTrue(form.is_valid())
