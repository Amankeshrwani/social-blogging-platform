from django.contrib import admin

# Register your models here.
from .models import Users, Post, Comment
admin.site.register(Users)
admin.site.register(Post)
admin.site.register(Comment)