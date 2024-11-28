from django.db import models
import datetime
from django.contrib.auth.models import User 


class Signup(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, default="default_user")  # Set a default username
    email = models.EmailField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to='static/profile_pictures/', null=True, blank=True)
    pwd = models.CharField(max_length=128)
    date = models.DateField(default=datetime.date.today)  # Set default to current date

    def __str__(self):
        return self.username


class CommunityPost(models.Model):
    # Topic details
    topic = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    content = models.TextField()

    # Stats for the post
    replies = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    activity_time = models.DateTimeField(auto_now=True)

    # Linking to the User model
    Signup = models.ForeignKey(Signup, on_delete=models.CASCADE)

    # Optionally, you can add additional fields such as tags or badges
    tags = models.ManyToManyField('Tag', blank=True)
    
    def __str__(self):
        return self.topic

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name