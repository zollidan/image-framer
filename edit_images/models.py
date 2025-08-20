import uuid
from django.db import models

class Image(models.Model):
    image_url = models.URLField(max_length=200)
    original_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.original_name