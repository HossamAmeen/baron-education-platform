from rest_framework.viewsets import ModelViewSet
from course.filters import SubjectFilter
from course.models import (City, Country, Course, EducationStage, Group,
                           Lesson, Semester, Subject)
from course.serializer import (CitySerializer, CourseSerializer,
                               EducationStageSerializer, GroupSerializer,
                               LessonSerializer, ListCourseSerializer,
                               SemesterSerializer, SubjectSerializer)
from django_filters.rest_framework import DjangoFilterBackend

class CountryViewSet(ModelViewSet):
    queryset = Country.objects.order_by('-id')
    serializer_class = CitySerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.order_by('-id')
    serializer_class = CitySerializer

class EducationStageViewSet(ModelViewSet):
    queryset = EducationStage.objects.prefetch_related( 'educationgrade_set__semester_set').order_by('-id')
    serializer_class = EducationStageSerializer


class SemesterViewSet(ModelViewSet):
    queryset = Semester.objects.order_by('-id')
    serializer_class = SemesterSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.order_by('-id')
    serializer_class = GroupSerializer


class CourseViweSet(ModelViewSet):
    queryset = Course.objects.order_by('-id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListCourseSerializer
        return CourseSerializer


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.order_by('-id')
    serializer_class = LessonSerializer


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.order_by('-id')
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter
