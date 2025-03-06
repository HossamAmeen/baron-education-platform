from datetime import date

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker

from configuration.models import Configuration, Review, Slider
from course.models import (Country, Course, EducationGrade,
                           EducationStage, Lesson, Semester, Subject, Teacher)


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
        subjects =self.generate_subjects(fake, semesters)
        self.generate_courses_and_lessons(fake, subjects)

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

        self.stdout.write(self.style.SUCCESS('Fake data generation complete! 🎉'))
        return Semester.objects.all()

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
            else:
                subject.save()
        return Subject.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Subject "{subject.name}" created for semester "{semester}" with image 1024x480!'))
    
    def generate_courses_and_lessons(self, fake, subjects):
        teacher = Teacher.objects.create(
                    first_name=fake.name(),
                    phone=fake.phone_number(),
                    username=fake.word() + str(fake.random_int(min=1, max=100)),
                    password=fake.word(),
                    email=fake.email(),
                    address=fake.address()
                )
        for _ in range(10):
            name = fake.catch_phrase()
            description = fake.text()
            available = fake.boolean()
            subject = fake.random_element(elements=subjects)
            course = Course.objects.create(
                name=name,
                description=description,
                available=available,
                start_date=fake.date_between(start_date=date(2025,4, 1), end_date="+1y"),
                hours_count=fake.random_int(min=1, max=100),
                duration=fake.random_int(min=1, max=100),
                price=fake.random_int(min=1, max=100),
                currency=fake.random_element(elements=Course.CurrencyCHOICES),
                image=subject.image,
                teacher=teacher,
                subject=subject
            )

            for _ in range(10):
                lesson = Lesson.objects.create(
                    title=fake.sentence(nb_words=6),
                    date=fake.date_between(start_date=date(2025,4, 1), end_date="+1y"),
                    time=fake.time_object(),
                    explanation_file=f"media/{fake.file_name(extension='pdf')}",
                    test_link=fake.url(),
                    video_link=fake.url(),
                    course=course,
                )
        self.stdout.write(self.style.SUCCESS(f'generate courses and lessons'))