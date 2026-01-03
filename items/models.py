from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    ITEM_TYPE_CHOICES = [
        ('Lost', 'Lost'),
        ('Found', 'Found'),
    ]

    item_type = models.CharField(max_length=5, choices=ITEM_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=100, help_text="Enter your email or phone number")
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_type}: {self.name}"