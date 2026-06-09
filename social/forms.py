from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]