from django.db.models import F
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

from users.models import User, Student


class MyTokenPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.get_role()
        token['email'] = user.email
        return token


class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"})
        attrs['password'] = make_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        return super().create(validated_data)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'gender', 'parent_phone', 'phone', 'email', 'password', 'password_confirmation']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        write_only=True,
        error_messages={'invalid':
                        ('Password must be at least 8 characters long with at least one capital letter and symbol')}) # noqa
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"})
        return attrs


class updatedStudentProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    password_confirmation = serializers.CharField(write_only=True, required=False)


    def validate(self, attrs):
        if attrs.get("password"):
            if not attrs.get("password_confirmation"):
                raise serializers.ValidationError(
                    {"password_confirmation": "This field is required when setting a new password."}
                )
            if attrs.get("password") != attrs.get("password_confirmation"):
                raise serializers.ValidationError(
                    {"password_confirmation": "Passwords do not match."}
                )
            attrs['password'] = make_password(attrs["password"])
        return attrs

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'parent_phone', 'phone',  'email', 'gender', 'password', 'password_confirmation']
