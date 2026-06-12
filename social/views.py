from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, AddCode, Profile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Connection
from .forms import ProfilePictureForm
from django.contrib import messages
from .models import ForumTopic, ForumReply
from .forms import ForumTopicForm, ForumReplyForm
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
        form = PostForm(request.POST, request.FILES)
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
@login_required
def bluetooth_add_friend(request):
    message = ""
    if request.method == "POST":
        code = request.POST.get("code")
        add_code = get_object_or_404(
            AddCode,
            code=code,
            used=False
        )
        if add_code.is_expired():
            message = "This code expired."
        elif add_code.user == request.user:
            message = "You cannot add yourself."
        else:
            other_user = add_code.user
            Connection.objects.get_or_create(
                from_user=request.user,
                to_user=other_user
            )
            Connection.objects.get_or_create(
                from_user=other_user,
                to_user=request.user
            )
            add_code.used = True
            add_code.save()
            message = f"You are now friends with {other_user.username}."
    return render(request, "social/bluetooth_add_friend.html", {
        "message": message
    })
@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    friend_count = Connection.objects.filter(from_user=request.user).count()
    if request.method == "POST":
        form = ProfilePictureForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            return redirect("/profile/")
    else:
        form = ProfilePictureForm(instance=profile)
    posts = Post.objects.filter(
        author=request.user
    ).order_by("-created_at")
    return render(request, "social/profile.html", {
        "profile": profile,
        "posts": posts,
        "form": form,
        "friend_count": friend_count,
    })
@login_required
def remove_friend(request, username):
    other_user = get_object_or_404(User, username=username)
    if request.method == "POST":
        Connection.objects.filter(
            from_user=request.user,
            to_user=other_user
        ).delete()
        Connection.objects.filter(
            from_user=other_user,
            to_user=request.user
        ).delete()
    return redirect("/friends/")
@login_required
def reply_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        text = request.POST.get("text")
        Comment.objects.create(
            post=post,
            author=request.user,
            text=text
        )
    return redirect("/")
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST" and post.author == request.user:
        post.delete()
    return redirect("/")
@login_required
def forum_list(request):
    topics = ForumTopic.objects.all().order_by("-created_at")
    return render(request, "social/forum_list.html", {"topics": topics})
@login_required
def create_topic(request):
    if request.method == "POST":
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect("/forums/")
    else:
        form = ForumTopicForm()
    return render(request, "social/create_topic.html", {"form": form})
@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    replies = ForumReply.objects.filter(topic=topic).order_by("created_at")
    if request.method == "POST":
        form = ForumReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = topic
            reply.author = request.user
            reply.save()
            return redirect(f"/forums/{topic.id}/")
    else:
        form = ForumReplyForm()
    return render(request, "social/topic_detail.html", {
        "topic": topic,
        "replies": replies,
        "form": form,
    })
@login_required
def receive_friend_code(request):
    code = AddCode.generate_code()
    AddCode.objects.create(
        user=request.user,
        code=code
    )
    return render(request, "social/receive_friend_code.html", {
        "code": code
    })