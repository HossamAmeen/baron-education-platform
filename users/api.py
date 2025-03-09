from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from users.models import Admin, Manager, Student, Teacher
from users.serializers import (AdminSerializer, ManagerSerializer,
                               StudentSerializer, TeacherSerializer)
from course.serializers import StudentCourseSerializer
from course.models import Course
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class AdminViewSet(ModelViewSet):
    schema = None
    queryset = Admin.objects.order_by('-id')
    serializer_class = AdminSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'email']


class TeacherViewSet(ModelViewSet):
    schema = None
    queryset = Teacher.objects.order_by('-id')
    serializer_class = TeacherSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'email']


class StudentViewSet(ModelViewSet):
    schema = None
    queryset = Student.objects.order_by('-id')
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'email']


class ManagerViewSet(ModelViewSet):
    schema = None
    queryset = Manager.objects.order_by('-id')
    serializer_class = ManagerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'email']


class StudentCourseListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentCourseSerializer

    def get_queryset(self):
        return Course.objects.filter(student=self.request.user)
