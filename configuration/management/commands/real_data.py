# flake8: noqa
from django.core.management.base import BaseCommand

from course.models import Country, EducationGrade, EducationStage, Semester
from users.models import User


class Command(BaseCommand):
    help = "Generates real data for the "

    def handle(self, *args, **kwargs):

        # create developer account
        owner = User.objects.filter(email="hosamameen948@gmail.com")
        if not owner.exists():
            owner = User.objects.create(
                first_name="hosam",
                phone="01010079798",
                password="admin",
                email="hosamameen948@gmail.com",
            )
            owner.set_password("admin")
            owner.save()

        # create country data
        egypt = Country.objects.create(name="مصر", code="EG")
        saudi_arabia = Country.objects.create(name="السعودية", code="SA")

        # create education stage data
        EducationStage.objects.create(name="المرحلة التعليمية", country=egypt)
        EducationStage.objects.create(name="المرحلة التعليمية", country=saudi_arabia)

        # create education grade data
        EducationGrade.objects.create(name="المرحلة التعليمية", education_stage=EducationStage.objects.get(name="المرحلة التعليمية", country=egypt))
        EducationGrade.objects.create(name="المرحلة التعليمية", education_stage=EducationStage.objects.get(name="المرحلة التعليمية", country=saudi_arabia))

        # create semester data
        Semester.objects.create(name="الsemester", education_grade=EducationGrade.objects.get(name="المرحلة التعليمية", education_stage=EducationStage.objects.get(name="المرحلة التعليمية", country=egypt)))
        Semester.objects.create(name="الsemester", education_grade=EducationGrade.objects.get(name="المرحلة التعليمية", education_stage=EducationStage.objects.get(name="المرحلة التعليمية", country=saudi_arabia)))
        self.stdout.write(
            self.style.SUCCESS(f"generate developer account")
        )
