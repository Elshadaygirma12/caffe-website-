from django.contrib import admin

# Register your models here.

from .models import MenuItem, GalleryImage, Testimonial

admin.site.register(MenuItem)
admin.site.register(GalleryImage)
admin.site.register(Testimonial)