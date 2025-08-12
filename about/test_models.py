from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from about.models import About, CollaborateRequest


class AboutModelTest(TestCase):
    """Test cases for the About model"""

    def setUp(self):
        """Set up test data"""
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.about = About.objects.create(
            author=self.user,
            title="Test About",
            content="Test Content"
        )

    def test_about_creation(self):
        """Test that an about instance can be created with valid data"""
        self.assertIsInstance(self.about, About)
        self.assertEqual(self.about.title, "Test About")
        self.assertEqual(self.about.content, "Test Content")

    def test_about_string_representation(self):
        """Test the string representation of the about model"""
        self.assertEqual(str(self.about), "Test About")

    def test_about_title_unique_constraint(self):
        """Test that title must be unique"""
        # Create another about instance with the same title
        with self.assertRaises(ValidationError):
            about = About(
                author=self.user,
                title="Test About",
                content="Another Test Content"
            )
            about.full_clean()  # This will raise ValidationError

    def test_about_title_max_length(self):
        """Test that title respects max_length constraint"""
        about = About(
            author=self.user,
            title="A" * 201,
            content="Test Content"
        )
        with self.assertRaises(ValidationError):
            about.full_clean()

    def test_about_default_profile_image(self):
        """Test that about has default placeholder image"""
        about = About(
            author=self.user,
            title="Test About",
            content="Test Content"
        )
        self.assertEqual(about.profile_image, "placeholder")

    def test_about_updated_on_auto_set(self):
        """Test that updated_on is automatically updated when the instance is changed"""
        # Update the existing about instance created in setUp
        old_updated_on = self.about.updated_on
        self.about.content = "Updated Content"
        self.about.save()
        self.about.refresh_from_db()
        self.assertNotEqual(self.about.updated_on, old_updated_on)

    def test_about_user_relationship(self):
        """Test the OneToOne relationship with User"""
        self.assertEqual(self.about.author, self.user)

    def test_about_cascade_delete(self):
        """Test that about is deleted when user is deleted"""
        self.user.delete()
        self.assertFalse(About.objects.filter(id=self.about.id).exists())

    def test_about_one_per_user(self):
        """Test that only one about entry per user is allowed"""
        # Create another about instance for the same user
        with self.assertRaises(ValidationError):
            about = About(
                author=self.user,
                title="Another Test About",
                content="Another Test Content"
            )
            about.full_clean()  # This will raise ValidationError


class CollaborateRequestModelTest(TestCase):
    """Test cases for the CollaborateRequest model"""

    def setUp(self):
        """Set up test data"""
        self.request = CollaborateRequest.objects.create(
            name="Test User",
            email="test@example.com",
            message="Test Message"
        )

    def test_collaborate_request_creation(self):
        """Test that a collaborate request can be created with valid data"""
        self.assertIsInstance(self.request, CollaborateRequest)
        self.assertEqual(self.request.name, "Test User")
        self.assertEqual(self.request.email, "test@example.com")
        self.assertEqual(self.request.message, "Test Message")

    def test_collaborate_request_string_representation(self):
        """Test the string representation of the collaborate request"""
        self.assertEqual(str(self.request), f"Collaboration request from {self.request.name}")

    def test_collaborate_request_name_max_length(self):
        """Test that name respects max_length constraint"""
        # Create a collaborate request with a long name
        long_name = "A" * 201
        with self.assertRaises(ValidationError):
            request = CollaborateRequest(
                name=long_name,
                email="test@example.com",
                message="Test Message"
            )
            request.full_clean()

    def test_collaborate_request_email_validation(self):
        """Test that email field validates email format"""
        invalid_emails = [
            "plainaddress",
            "@missingusername.com",
            "username@.com",
            "username@domain..com"
        ]
        for email in invalid_emails:
            with self.assertRaises(ValidationError):
                request = CollaborateRequest(
                    name="Test User",
                    email=email,
                    message="Test Message"
                )
                request.full_clean()

    def test_collaborate_request_default_read_status(self):
        """Test that read field defaults to False"""
        request = CollaborateRequest(
            name="Test User",
            email="test@example.com",
            message="Test Message"
        )
        self.assertFalse(request.read)

    def test_collaborate_request_required_fields(self):
        """Test that required fields cannot be empty"""
        with self.assertRaises(ValidationError):
            request = CollaborateRequest(
                name="",
                email="test@example.com",
                message="Test Message"
            )
            request.full_clean()

        with self.assertRaises(ValidationError):
            request = CollaborateRequest(
                name="Test User",
                email="",
                message="Test Message"
            )
            request.full_clean()

        with self.assertRaises(ValidationError):
            request = CollaborateRequest(
                name="Test User",
                email="test@example.com",
                message=""
            )
            request.full_clean()

    def test_collaborate_request_read_status_toggle(self):
        """Test that read status can be toggled"""
        request = CollaborateRequest(
            name="Test User",
            email="test@example.com",
            message="Test Message"
        )
        request.full_clean()
        self.assertFalse(request.read)
        request.read = True
        self.assertTrue(request.read)
