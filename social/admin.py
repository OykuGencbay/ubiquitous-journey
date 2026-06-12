from django.contrib import admin
from .models import Profile, Connection, AddCode, Post, Comment
from .models import ForumTopic, ForumReply
admin.site.register(Profile)
admin.site.register(Connection)
admin.site.register(AddCode)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ForumTopic)
admin.site.register(ForumReply)