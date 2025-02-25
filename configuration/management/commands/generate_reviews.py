from django.core.management.base import BaseCommand
from faker import Faker
from configuration.models import Review

class Command(BaseCommand):
    help = 'Generates 20 rows of garbage data for the Review model'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(20):
            Review.objects.create(
                name=fake.name(),
                description=fake.text(),
                rate=fake.random_int(min=1, max=5),
                ordering=fake.random_int(min=1, max=100)
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated 20 reviews'))
