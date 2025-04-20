from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not phone:
            raise ValueError("The Phone field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, phone, password, **extra_fields)


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
