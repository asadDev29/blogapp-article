from django.test import TestCase
from .models import Writer, Article
from django.contrib.auth.models import User

class BlogAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.writer = Writer.objects.create(user=self.user)

    def test_writer_creation(self):
        self.assertEqual(str(self.writer), 'testuser')

    def test_article_creation(self):
        article = Article.objects.create(title="Test Article", content="Test Content", written_by=self.writer)
        self.assertEqual(article.title, "Test Article")
