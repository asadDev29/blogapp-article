from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),  # Your app URLs
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Add this for login
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add this for logout
]
