from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(
        template_name="social/login.html"
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("generate-code/", views.generate_code, name="generate_code"),
    path("user/<str:username>/", views.user_profile, name="user_profile"),
    path("friends/", views.friend_list, name="friend_list"),
    path("nearby/", views.nearby, name="nearby"),
    path("bluetooth-add/", views.bluetooth_add_friend, name="bluetooth_add_friend"),
    path("user/<str:username>/remove-friend/", views.remove_friend, name="remove_friend"),
    path("reply/<int:post_id>/", views.reply_to_post, name="reply_to_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("forums/", views.forum_list, name="forum_list"),
    path("forums/new/", views.create_topic, name="create_topic"),
    path("forums/<int:topic_id>/", views.topic_detail, name="topic_detail"),
    path("receive-code/", views.receive_friend_code, name="receive_friend_code"),
    path("bluetooth-add/", views.bluetooth_add_friend, name="bluetooth_add_friend"),
]