from django.db import models

from users.models import Student, Teacher


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)


class City(models.Model):
    name = models.CharField(max_length=100)

class EducationStage(models.Model):
    name = models.CharField(max_length=100)


class EducationGrade(models.Model):
    name = models.CharField(max_length=100)
    education_stage = models.ForeignKey(EducationStage, on_delete=models.CASCADE)


class Semester(models.Model):
    name = models.CharField(max_length=100)
    education_grade = models.ForeignKey(EducationGrade, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField()


class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student)


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/')
    start_date = models.DateField()
    hours_count = models.IntegerField()
    duration = models.IntegerField()
    semster = models.ForeignKey(Semester, on_delete=models.CASCADE)
