from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import AddCode
from .forms import PostForm
from .models import Post, AddCode, Profile, Connection
def home(request):
    if request.user.is_authenticated:
        friend_ids = Connection.objects.filter(
            from_user=request.user
        ).values_list("to_user_id", flat=True)
        posts = Post.objects.filter(
            author_id__in=list(friend_ids) + [request.user.id]
        ).order_by("-created_at")
    else:
        posts = Post.objects.none()
    if request.method == "POST" and request.user.is_authenticated:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/")
    else:
        form = PostForm()
    return render(request, "social/home.html", {
        "form": form,
        "posts": posts,
    })
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "social/register.html", {"form": form})
@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(author=request.user).order_by("-created_at")
    return render(request, "social/profile.html", {
        "profile": profile,
        "posts": posts,
    })
@login_required
def generate_code(request):
    code = AddCode.generate_code()
    AddCode.objects.create(
        user=request.user,
        code=code
    )
    return render(
        request,
        "social/generate_code.html",
        {"code": code}
    )
@login_required
def friend_list(request):
    connections = Connection.objects.filter(from_user=request.user)
    return render(request, "social/friend_list.html", {
        "connections": connections
    })
@login_required
def nearby(request):
    return render(request, "social/nearby.html")
from django.contrib.auth.models import User
def user_profile(request, username):
    profile_user = User.objects.get(username=username)
    profile, created = Profile.objects.get_or_create(user=profile_user)
    posts = Post.objects.filter(author=profile_user).order_by("-created_at")
    return render(request, "social/user_profile.html", {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
    })