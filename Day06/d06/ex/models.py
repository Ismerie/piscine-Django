from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Tip(models.Model):
    content = models.TextField()
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    date = models.DateTimeField(auto_now=True)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)

class Vot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
