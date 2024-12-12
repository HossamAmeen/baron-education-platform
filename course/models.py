from django.db import models

from users.models import Student, Teacher


class City(models.Model):
    name = models.CharField(max_length=100)


class Semester(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()


class Group(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField()


class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student)
