from django.db import models
from payments.models import Transaction
from users.models import Student, Teacher
from django_extensions.db.models import TimeStampedModel


class Country(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)


class EducationStage(TimeStampedModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

class EducationGrade(TimeStampedModel):
    name = models.CharField(max_length=100)
    education_stage = models.ForeignKey(EducationStage, on_delete=models.CASCADE)


class Semester(TimeStampedModel):
    name = models.CharField(max_length=100)
    education_grade = models.ForeignKey(EducationGrade, on_delete=models.CASCADE)


class Group(TimeStampedModel):
    name = models.CharField(max_length=100)
    time = models.DateTimeField()

class Subject(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)


class Course(TimeStampedModel):
    class CurrencyCHOICES(models.TextChoices):
        EGP = 'EGP'
        KSA = 'KSA'

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    available = models.BooleanField(default=True)
    start_date = models.DateField()
    hours_count = models.IntegerField()
    duration = models.IntegerField()
    price = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CurrencyCHOICES.choices, default=CurrencyCHOICES.EGP)
    image = models.ImageField(upload_to='media/')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Lesson(TimeStampedModel):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    explanation_file = models.FileField(upload_to='media/')
    test_link = models.URLField()
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class StudentCourse(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
