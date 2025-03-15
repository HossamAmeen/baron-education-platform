from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import Admin, Manager, Student, Teacher, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone',
                  'gender', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value):
        return make_password(value)


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = ['id', 'is_active',
                  'full_name', 'phone', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value):
        return make_password(value)


class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manager
        fields = ['id', 'is_active',
                  'full_name', 'phone', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value):
        return make_password(value)


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ['id', 'is_active', 'address',
                  'full_name', 'phone', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value):
        return make_password(value)


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['id', 'is_active', 'parent_phone', 'address',
                  'full_name', 'phone', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value):
        return make_password(value)
