# Generated by Django 4.2 on 2024-11-17 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_signup_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/profile_pictures/'),
        ),
    ]
