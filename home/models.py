from django.db import models
import datetime

class Signup(models.Model):
    username = models.CharField(max_length=128, default="default_user")  # Set a default username
    email = models.EmailField(max_length=255, null=False, blank=False)
    pwd = models.CharField(max_length=128)
    date = models.DateField(default=datetime.date.today)  # Set default to current date

    def __str__(self):
        return self.username
