from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Slider(models.Model):
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='media/')
    ordering = models.IntegerField()
    link = models.URLField(null=True)


class Review(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    rate = models.IntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(5)])
    ordering = models.IntegerField()


class ContactUs(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    description = models.TextField()


class Configuration(models.Model):
    eg_number = models.CharField(max_length=15)
    ksa_number = models.CharField(max_length=15)
    eg_adderss = models.CharField(max_length=100)
    ksa_adderss = models.CharField(max_length=100)
    email = models.EmailField()
    about_us = models.TextField()
    our_vision = models.TextField()
    our_mission = models.TextField()
    student_counter = models.IntegerField()
    teacher_counter = models.IntegerField()
    partner_counter = models.IntegerField()
    meta = models.URLField(null=True)
    twitter = models.URLField(null=True)
    linkedin = models.URLField(null=True)
    googel = models.URLField(null=True)
    footer_description = models.TextField()
