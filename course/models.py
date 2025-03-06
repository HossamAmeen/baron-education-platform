from django.db import models

from users.models import Student, Teacher


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)


class EducationStage(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

class EducationGrade(models.Model):
    name = models.CharField(max_length=100)
    education_stage = models.ForeignKey(EducationStage, on_delete=models.CASCADE)


class Semester(models.Model):
    name = models.CharField(max_length=100)
    education_grade = models.ForeignKey(EducationGrade, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField()

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)


class Course(models.Model):
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
    student = models.ManyToManyField(Student)


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
