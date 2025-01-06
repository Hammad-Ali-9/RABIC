from django.core.management.base import BaseCommand
from home.models import Category

class Command(BaseCommand):
    help = 'Creates initial categories'

    def handle(self, *args, **kwargs):
        categories = [
            "General",
            "Technical",
            "Help",
            "Announcements",
            "Discussion",
            "Questions"
        ]

        for name in categories:
            Category.objects.get_or_create(name=name)
            self.stdout.write(self.style.SUCCESS(f'Successfully created category "{name}"')) 