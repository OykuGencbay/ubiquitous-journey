from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Profile, Comment
from .models import ForumTopic, ForumReply
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text", "image"]
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture"]
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ["title", "body"]
class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ["text"]