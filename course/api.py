from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from course.filters import SubjectFilter
from course.models import (Country, Course, EducationStage, Group, Lesson,
                           Semester, Subject)
from course.serializer import (CountrySerializer, CourseSerializer,
                               EducationStageSerializer, GroupSerializer,
                               LessonSerializer, ListCourseSerializer,
                               RetrieveCourseSerializer, SemesterSerializer,
                               SubjectSerializer)


class CountryListAPIView(ListAPIView):
    queryset = Country.objects.prefetch_related('educationstage_set__educationgrade_set__semester_set').order_by('-id')
    serializer_class = CountrySerializer


class EducationStageViewSet(ModelViewSet):
    schema = None
    queryset = EducationStage.objects.prefetch_related( 'educationgrade_set__semester_set').order_by('-id')
    serializer_class = EducationStageSerializer


class SemesterViewSet(ModelViewSet):
    schema = None
    queryset = Semester.objects.order_by('-id')
    serializer_class = SemesterSerializer


class GroupViewSet(ModelViewSet):
    schema = None
    queryset = Group.objects.order_by('-id')
    serializer_class = GroupSerializer


class CourseViweSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Course.objects.order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return ListCourseSerializer
        if self.action == 'retrieve':
            return RetrieveCourseSerializer
        return CourseSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset.prefetch_related(
                Prefetch(
                    'lesson_set',
                    queryset=Lesson.objects.order_by('-id'),
                    to_attr='lessons')
                )
        return self.queryset
class LessonViewSet(ModelViewSet):
    schema = None
    queryset = Lesson.objects.order_by('-id')
    serializer_class = LessonSerializer


class SubjectViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Subject.objects.prefetch_related(
        Prefetch(
            'course_set', 
            queryset=Course.objects.filter(available=True)[:1], 
            to_attr='available_courses'
        )
    ).order_by('-id')

    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter
