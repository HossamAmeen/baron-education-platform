from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import Admin, Manager, Student, Teacher, UserAccount


class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'password', 'phone',
                  'gender', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate(self, data):
        email = data.get('email')
        phone = data.get('phone')

        if not email and not phone:
            return serializers.ValidationError(
                "Please Enter  Email or Phone Number!")

        if email and UserAccount.objects.filter(email=email).exists():
            return serializers.ValidationError("Email Already Exists!")

        if phone and UserAccount.objects.filter(phone=phone).exists():
            return serializers.ValidationError("Phone Number Already Exists!")

        return data

    def validate_password(self, value):
        return make_password(value)


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = ['id', 'username', 'is_active',
                  'full_name', 'phone', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value):
        return make_password(value)


class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manager
        fields = ['id', 'username', 'is_active',
                  'full_name', 'phone', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value):
        return make_password(value)


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ['id', 'username', 'is_active', 'address',
                  'full_name', 'phone', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value):
        return make_password(value)


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['id', 'username', 'is_active', 'parent_phone', 'address',
                  'full_name', 'phone', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value):
        return make_password(value)
