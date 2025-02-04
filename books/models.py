# books/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    published_date = models.DateField(max_length=10)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title
