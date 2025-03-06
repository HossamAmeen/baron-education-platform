from django.contrib.auth.models import AbstractUser
from django.db import models


class UserAccount(AbstractUser):
    is_staff = date_joined = is_superuser = groups = user_permissions = None

    GENDER_CHOICES = [('male', 'ذكر'), ('female', 'أنثى')]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone']

    def get_role(self):
        if hasattr(self, 'admin'):
            return "admin"
        elif hasattr(self, 'manager'):
            return "manager"
        elif hasattr(self, 'teacher'):
            return "teacher"
        elif hasattr(self, 'student'):
            return "student"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email


class Admin(UserAccount):
    pass


class Manager(UserAccount):
    pass


class Teacher(UserAccount):
    address = models.CharField(max_length=100)


class Student(UserAccount):
    address = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=50)
