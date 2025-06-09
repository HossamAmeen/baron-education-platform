from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from auth.models import PasswordReset
from auth.serializers import (
    LoginSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer,
    StudentRegisterSerializer,
    updatedStudentProfileSerializer,
)
from users.models import User


class RegisterAPI(generics.CreateAPIView):
    authentication_classes = []
    serializer_class = StudentRegisterSerializer


class LoginAPI(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(
            Q(email=serializer.validated_data["username"])
            | Q(phone=serializer.validated_data["username"])
        ).first()
        if not user or not user.check_password(
            serializer.validated_data["password"]
        ):  # noqa
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        tokens = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(tokens.access_token),
                "refresh": str(tokens),
            },
            status=status.HTTP_200_OK,
        )


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            email__iexact=serializer.validated_data["email"]
        ).first()
        if user:
            if PasswordReset.objects.filter(email=user.email).count() > 2:
                return Response(
                    {"message": "we send url to your email."}, status=status.HTTP_200_OK
                )

            token = PasswordResetTokenGenerator().make_token(user)
            PasswordReset.objects.create(email=user.email, token=token)

            return Response(
                {"message": "we send url to your email.", "success": token},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "User with credentials not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_password = PasswordReset.objects.filter(token=token).first()

        if not reset_password:
            return Response({"error": "Invalid token"}, status=400)

        user = User.objects.filter(email=reset_password.email).first()

        if user:
            user.set_password(request.data["new_password"])
            user.save()

            reset_password.delete()

            return Response({"success": "Password updated"})
        else:
            return Response({"error": "No user found"}, status=404)


class StudentProfileView(generics.GenericAPIView):
    serializer_class = updatedStudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(request.user.student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = self.serializer_class(
            request.user.student, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
