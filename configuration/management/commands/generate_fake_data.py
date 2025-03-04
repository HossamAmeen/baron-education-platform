import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker

from configuration.models import Configuration, Review, Slider
from course.models import (City, Country, EducationGrade, EducationStage,
                           Semester, Subject)


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
        semesters = self.generate_semesters(fake)
        self.generate_subjects(fake, semesters)
        self.stdout.write(self.style.SUCCESS('Successfully generated 20 reviews'))

    def generate_sliders(self, fake):
        for _ in range(10):
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

    def generate_subjects(self, fake, semesters):
        for _ in range(10):
            name = fake.catch_phrase()
            description = fake.text()
            available = fake.boolean()

            # Randomly pick a semester
            semester = fake.random_element(elements=semesters)

            # Fetch a random placeholder image with specific dimensions
            image_url = fake.image_url()
            image_response = requests.get(image_url)

            subject = Subject(
                name=name,
                description=description,
                available=available,
                semester=semester
            )

            # Save image to ImageField
            if image_response.status_code == 200:
                subject.image.save(
                    f'{fake.word()}.png', 
                    ContentFile(image_response.content), 
                    save=True
                )

        self.stdout.write(self.style.SUCCESS(f'Subject "{subject.name}" created for semester "{semester}" with image 1024x480!'))

    def generate_semesters(self, fake):
         # Create fixed countries
        egypt, _ = Country.objects.get_or_create(name="Egypt", code="EG")
        saudi_arabia, _ = Country.objects.get_or_create(name="Saudi Arabia", code="SA")

        self.stdout.write(self.style.SUCCESS(f'Fixed Country: {egypt.name} (EG)'))
        self.stdout.write(self.style.SUCCESS(f'Fixed Country: {saudi_arabia.name} (SA)'))

        # Generate Education Stages for fixed countries
        for country in [egypt, saudi_arabia]:
            for _ in range(3):
                stage = EducationStage.objects.create(
                    name=fake.word() + " Stage",
                    country=country
                )
                self.stdout.write(self.style.SUCCESS(f'  ↳ Created Education Stage: {stage.name} in {country.name}'))

                # Generate Education Grades for each Stage
                for _ in range(3):
                    grade = EducationGrade.objects.create(
                        name=fake.word() + " Grade",
                        education_stage=stage
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created Education Grade: {grade.name} in {stage.name}'))

                    # Generate Semesters for each Grade
                    for i in range(2):
                        semester = Semester.objects.create(
                            name=f"Semester {i + 1}",
                            education_grade=grade
                        )
                        self.stdout.write(self.style.SUCCESS(f'Created Semester: {semester.name} in {grade.name}'))

            # Generate Cities
            for _ in range(2):
                city = City.objects.create(name=fake.city(), country=egypt)
                self.stdout.write(self.style.SUCCESS(f'Created City: {city.name}'))

        self.stdout.write(self.style.SUCCESS('Fake data generation complete! 🎉'))
        return Semester.objects.all()
