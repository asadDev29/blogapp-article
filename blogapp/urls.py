from django.urls import path
from .views import DashboardView, ArticleCreateView, ArticleDetailView, ArticleApprovalView, ArticlesEditedView,SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('article/create/', ArticleCreateView.as_view(), name='create_article'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article-approval/', ArticleApprovalView.as_view(), name='article_approval'),
    path('articles-edited/', ArticlesEditedView.as_view(), name='articles_edited'),
]
