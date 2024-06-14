from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Room (models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return f"Message(from:{self.user.username})(Room:{self.room.label})[content:{self.message}]"