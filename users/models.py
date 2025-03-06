from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not phone:
            raise ValueError('The Phone field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('username', email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone, password, **extra_fields)


class UserAccount(AbstractUser):
    date_joined = is_superuser = groups = user_permissions = None

    GENDER_CHOICES = [('male', 'ذكر'), ('female', 'أنثى')]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

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
