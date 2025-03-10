from rest_framework import serializers

from course.models import (Country, Course, EducationGrade, EducationStage,
                           Group, Lesson, Semester, Subject)
from payments.models import Transaction


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


class EducationGradeSerializer(serializers.ModelSerializer):
    semesters = SemesterSerializer(source="semester_set", many=True)

    class Meta:
        model = EducationGrade
        fields = "__all__"


class EducationStageSerializer(serializers.ModelSerializer):
    grades = EducationGradeSerializer(source="educationgrade_set", many=True)

    class Meta:
        model = EducationStage
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    education_stages = EducationStageSerializer(source="educationstage_set", many=True)

    class Meta:
        model = Country
        fields = '__all__'


class SingleCouurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'date', 'time', 'explanation_file',
                  'test_link', 'video_link']


class RetrieveCourseSerializer(serializers.ModelSerializer):
    is_paid = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True)


    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'start_date', 'hours_count', 'duration', 'price',
                  'currency', 'image', 'lessons', 'is_paid']

    def get_is_paid(self, obj):
        user = self.context['request'].user
        if user and user.is_authenticated  and user.get_role() == "student" and obj.student_courses.filter(
                student=user, transaction__status=Transaction.TransactionStatus.PAID).exists():
            return True
        return False

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Hide lessons if not paid
        if not representation['is_paid']:
            representation['lessons'] = []
        
        return representation


class ListCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'start_date', 'hours_count', 'duration',
                  'price', 'currency', 'image']



class SubjectSerializer(serializers.ModelSerializer):
    available_course = SingleCouurseSerializer(source="available_courses", many=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'available', 'image', 'semester', 'available', 'available_course']


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'start_date', 'hours_count',
                  'duration', 'price', 'currency', 'image']
