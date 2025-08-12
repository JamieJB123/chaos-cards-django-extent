from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Model for cards

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=500)
    featured_image = CloudinaryField('image', default='placeholder', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    def __str__(self):
        return f'{self.title} by {self.user.username}'
