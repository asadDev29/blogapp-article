from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article, Writer
from django.utils import timezone
from django.db.models import Count, Q
from .forms import ArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth import login
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse

# Dashboard View
class DashboardView(LoginRequiredMixin, ListView):
    model = Writer
    template_name = 'dashboard.html'
    context_object_name = 'writers'

    def get_queryset(self):
        return Writer.objects.annotate(
            total_articles=Count('articles_written'),
            last_30_articles=Count('articles_written', filter=Q(articles_written__created_at__gte=timezone.now() - timezone.timedelta(days=30)))
        )

# Article Creation View
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'
    success_url = '/'

    def form_valid(self, form):
        # Ensure the logged-in user has a writer instance
        if not hasattr(self.request.user, 'writer'):
            Writer.objects.create(user=self.request.user)
        
        form.instance.written_by = self.request.user.writer
        return super().form_valid(form)

# Article Detail View
class ArticleDetailView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_detail.html'
    success_url = reverse_lazy('dashboard')  # Redirect to the dashboard after saving

    def get_object(self, queryset=None):
        # Make sure all writers can access the page
        return get_object_or_404(Article, pk=self.kwargs['pk'])

    def get_queryset(self):
        # Restrict editing access to writers who wrote the article or editors
        return Article.objects.filter(written_by=self.request.user.writer)


# Article Approval View (Editors Only)
class EditorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        print(" editor:",self.request.user.writer)
        return self.request.user.writer.is_editor

class ArticleApprovalView(EditorRequiredMixin, ListView):
    model = Article
    template_name = 'article_approval.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(status='DRAFT')
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        article_id = request.POST.get('article_id')

        # Check if an action is specified and article ID is provided
        if action and article_id:
            article = get_object_or_404(Article, id=article_id)

            if action == 'approve':
                self.approve_article(article)
            elif action == 'reject':
                self.reject_article(article)

        return HttpResponseRedirect(reverse('article_approval'))

    def approve_article(self, article):
        article.status = 'PUBLISHED'  # Change status to published
        article.edited_by = self.request.user.writer  # Set the editor who approved it
        article.save()

    def reject_article(self, article):
        article.status = 'REJECTED'  # Change status to rejected
        article.edited_by = self.request.user.writer  # Set the editor who rejected it
        article.save()

# Articles Edited (Editor History)
class ArticlesEditedView(EditorRequiredMixin, ListView):
    model = Article
    template_name = 'articles_edited.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(edited_by=self.request.user.writer)

# User signup
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()  # Save the user
        # Create a writer instance for the new user
        if not Writer.objects.filter(user=user).exists():
            Writer.objects.create(user=user)
        login(self.request, user)  # Automatically log the user in after signup
        return super().form_valid(form)