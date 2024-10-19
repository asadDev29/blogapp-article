from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Writer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_editor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Article(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('REJECTED', 'Rejected'),
    ]
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    written_by = models.ForeignKey(Writer, related_name='articles_written', on_delete=models.CASCADE)
    edited_by = models.ForeignKey(Writer, related_name='articles_edited', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})
