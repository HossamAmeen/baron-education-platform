from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import CustomUserManager


class User(AbstractUser):
    date_joined = groups = user_permissions = username = None

    class UserGender(models.TextChoices):
        MALE = "male", "ذكر"
        FEMALE = "female", "أنثى"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length=6, choices=UserGender.choices, default=UserGender.MALE
    )
    role = models.CharField(max_length=50, default="admin")
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = CustomUserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email


class Admin(User):
    pass


class Manager(User):
    pass


class Teacher(User):
    pass


class Student(User):
    parent_phone = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def save(self, *args, **kwargs):
        self.role = "student"
        self.is_staff = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name}({self.phone})"
