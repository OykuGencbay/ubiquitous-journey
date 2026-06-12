from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture"]
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]