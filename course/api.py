from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from course.filters import SubjectFilter
from course.models import (
    Country,
    Course,
    EducationStage,
    Group,
    Lesson,
    Semester,
    StudentCourse,
    Subject,
)
from course.serializers import (
    CountrySerializer,
    CourseSerializer,
    EducationStageSerializer,
    GroupSerializer,
    LessonSerializer,
    ListCourseSerializer,
    RetrieveCourseSerializer,
    SemesterSerializer,
    SubjectSerializer,
)
from payments.models import Transaction


class CountryListAPIView(ListAPIView):
    queryset = Country.objects.prefetch_related(
        "educationstage_set__educationgrade_set__semester_set"
    ).order_by("-id")
    serializer_class = CountrySerializer


class EducationStageViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = EducationStage.objects.prefetch_related(
        "educationgrade_set__semester_set"
    ).order_by("-id")
    serializer_class = EducationStageSerializer


class SemesterViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Semester.objects.order_by("-id")
    serializer_class = SemesterSerializer


class GroupViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Group.objects.order_by("-id")
    serializer_class = GroupSerializer


class CourseViweSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Course.objects.order_by("-id")

    def get_serializer_class(self):
        if self.action == "list":
            return ListCourseSerializer
        if self.action == "retrieve":
            return RetrieveCourseSerializer
        return CourseSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            self.queryset = self.queryset.filter(student_courses__student=self.request.user)
        return self.queryset


class LessonViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Lesson.objects.order_by("-id")
    serializer_class = LessonSerializer


class SubjectViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Subject.objects.prefetch_related(
        Prefetch(
            "course_set",
            queryset=Course.objects.filter(available=True)[:1],
            to_attr="available_courses",
        )
    ).order_by("-id")

    def get_queryset(self):
        if self.request.query_params.get("is_tahsili"):
            self.queryset = self.queryset.filter(is_tahsili=True)
        else:
            self.queryset = self.queryset.filter(is_tahsili=False)
            
        if self.request.query_params.get("is_kamiy"):
            self.queryset = self.queryset.filter(is_kamiy=True)
        else:
            self.queryset = self.queryset.filter(is_kamiy=False)
        return self.queryset

    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter
