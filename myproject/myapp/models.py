from django.db import models
from django.contrib.auth.models import User


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('blends', 'Signature Blends'),
        ('pastries', 'Freshly Baked Pastries'),
        ('treats', 'Gourmet Treats'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='blends')

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.alt_text or f"Gallery Image {self.id}"

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    testimonial_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)