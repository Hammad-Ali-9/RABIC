from django.db import models
import datetime

class Signup(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, default="default_user")
    email = models.EmailField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to='static/profile_pictures/', null=True, blank=True)
    pwd = models.CharField(max_length=128)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.username

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CommunityPost(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_DEFAULT, 
        default=1,  # Will use the first category (General) as default
        to_field='id'  # Explicitly specify the field to use for foreign key
    )
    content = models.TextField()
    replies = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    activity_time = models.DateTimeField(auto_now=True)
    Signup = models.ForeignKey(Signup, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return self.topic

    class Meta:
        ordering = ['-activity_time']

class UserActivity(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)  # 'login', 'post', 'comment', etc.
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'User Activities'

class LoginHistory(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-login_time']
        verbose_name_plural = 'Login Histories'