from django.db import models
from blog.models import Users

# Create your models here.

class Chat_list(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.ManyToManyField(Users, related_name='chat_users', blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between: {', '.join(user.username for user in self.users.all())}"


class Chat_message(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.ForeignKey(Chat_list, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_messages')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:20]}..."