from django.db import models
from django.contrib.auth.models import User




class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=75)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    image = models.ImageField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name