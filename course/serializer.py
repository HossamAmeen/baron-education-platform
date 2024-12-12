from rest_framework import serializers

from course.models import City, Course, Group, Semester
from users.serializers import StudentSerializer, TeacherSerializer


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class ListCourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    student = StudentSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'
