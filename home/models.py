from django.db import models

class Signup(models.Model):
    email = models.EmailField(max_length=255)  # Optional, as EmailField has default max_length
    pwd = models.CharField(max_length=128)  # Password field
    date = models.DateField(auto_now_add=True)

# Create your models here.
def __str__(self):
    return self.email

