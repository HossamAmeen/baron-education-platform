import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker

from configuration.models import Review, Slider, Configuration


class Command(BaseCommand):
    help = 'Generates 20 rows of garbage data for the Review model'

    def handle(self, *args, **kwargs):
        fake = Faker()
        config = Configuration.objects.create(
            eg_number=fake.phone_number()[:15],
            ksa_number=fake.phone_number()[:15],
            eg_adderss=fake.address()[:100],
            ksa_adderss=fake.address()[:100],
            email=fake.email(),
            about_us=fake.text(),
            our_vision=fake.text(),
            our_mission=fake.text(),
            student_counter=fake.random_int(min=0, max=10000),
            teacher_counter=fake.random_int(min=0, max=1000),
            partner_counter=fake.random_int(min=0, max=500),
            meta=fake.url(),
            twitter=fake.url(),
            linkedin=fake.url(),
            googel=fake.url(),
            footer_description=fake.text(),
        )

        self.stdout.write(self.style.SUCCESS(f'Configuration row with ID {config.id} created!'))

        self.generate_reviews(fake)
        self.generate_sliders(fake)
        self.stdout.write(self.style.SUCCESS('Successfully generated 20 reviews'))

    def generate_sliders(self, fake):
        for _ in range(10):  # Generate 10 fake records
            description = fake.text()
            ordering = fake.random_int(min=1, max=100)
            link = fake.url()

            # Download a random image
            image_url = fake.image_url()
            image_response = requests.get(image_url)

            slider = Slider(
                description=description,
                ordering=ordering,
                link=link
            )

            # Save image to ImageField
            if image_response.status_code == 200:
                slider.image.save(
                    f'{fake.word()}.jpg', 
                    ContentFile(image_response.content), 
                    save=True
                )

            self.stdout.write(self.style.SUCCESS(f'Slider {slider.id} created!'))

    def generate_reviews(self, fake):
        for _ in range(20):
            Review.objects.create(
                name=fake.name(),
                description=fake.text(),
                rate=fake.random_int(min=1, max=5),
                ordering=fake.random_int(min=1, max=100)
        )