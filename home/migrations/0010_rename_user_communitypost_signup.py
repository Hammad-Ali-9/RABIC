# Generated by Django 4.2 on 2024-11-28 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_tag_communitypost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='communitypost',
            old_name='user',
            new_name='Signup',
        ),
    ]