from django.db import models
# User Model
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# About Model

class About(models.Model):
    """
    Stores a single about me text
    """
    title = models.CharField(max_length=200, unique=True)
    profile_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name="about_entry")

    def __str__(self):
        return self.title

# Collaborate Model

class CollaborateRequest(models.Model):
    """
    Stores a single collaboration request message
    """
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)  # Standard email max length
    message = models.TextField(max_length=500)  # Add reasonable limit
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Collaboration request from {self.name}"
