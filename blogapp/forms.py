from django import forms
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']  # Only 'title' and 'content' are editable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If you want to display the status field but make it read-only in the form
        self.fields['status'] = forms.CharField(initial=self.instance.status, disabled=True, required=False)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
