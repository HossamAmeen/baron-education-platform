from django.db import models
from payments.models import Transaction
from users.models import Student, Teacher
from django_extensions.db.models import TimeStampedModel


class Country(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class EducationStage(TimeStampedModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Education Stages"

    def __str__(self):
        return self.name


class EducationGrade(TimeStampedModel):
    name = models.CharField(max_length=100)
    education_stage = models.ForeignKey(EducationStage, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Education Grades"

    def __str__(self):
        return self.name


class Semester(TimeStampedModel):
    name = models.CharField(max_length=100)
    education_grade = models.ForeignKey(EducationGrade, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Semesters"

    def __str__(self):
        return self.name


class Group(TimeStampedModel):
    name = models.CharField(max_length=100)
    time = models.DateTimeField()

class Subject(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Lesson(TimeStampedModel):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    explanation_file = models.FileField(upload_to='media/')
    test_link = models.URLField()
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Lessons"

    def __str__(self):
        return self.title

class StudentCourse(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_courses')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_courses')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
