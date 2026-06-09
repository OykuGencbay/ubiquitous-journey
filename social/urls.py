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
]