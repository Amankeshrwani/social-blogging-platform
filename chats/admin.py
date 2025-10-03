from django.contrib import admin

# Register your models here.
from .models import Chat_list, Chat_message
admin.site.register(Chat_list)
admin.site.register(Chat_message)