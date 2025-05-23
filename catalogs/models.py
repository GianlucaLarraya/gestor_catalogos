from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Catalog(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='catalogs')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalogs'
        indexes = [
            models.Index(fields=['uuid']),
        ]

    def __str__(self):
        return self.title

class Album(models.Model):
    id = models.BigAutoField(primary_key=True)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'albums'
        unique_together = ('catalog', 'title')

    def __str__(self):
        return self.title

class Photo(models.Model):
    id = models.BigAutoField(primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'photos'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title
