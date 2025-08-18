from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from auth.models import PasswordReset
from auth.serializers import (
    LoginSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer,
    StudentRegisterSerializer,
    updatedStudentProfileSerializer,
)
from shared.permisions import IsStudent
from users.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

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
        roles = serializer.validated_data.get("roles", ["student"])
        user = User.objects.filter(
            Q(email=serializer.validated_data["username"])
            | Q(phone=serializer.validated_data["username"])
        ).first()
        if not user or not user.check_password(
            serializer.validated_data["password"]
        ):  # noqa
            return Response(
                {"details": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        if user.role not in roles:
            return Response(
                {"details": "Invalid role"}, status=status.HTTP_401_UNAUTHORIZED
            )
        tokens = RefreshToken.for_user(user)
        user_data = {
            "id": user.id,
            "full_name": user.get_full_name(),
        }
        tokens = RefreshToken.for_user(user)
        tokens["user"] = user_data

        return Response(
            {
                "access": str(tokens.access_token),
                "refresh": str(tokens),
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": user.phone,
                    "email": user.email,
                    "gender": user.gender,
                    "role": user.role,
                },
            },
            status=status.HTTP_200_OK,
        )


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Generate token and uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Create reset URL
        rest_password_url = reverse("password_reset_confirm", args=[uid, token])

        # Send email
        subject = 'Password Reset Request'
        message = f'Click the link to reset your password: {request.build_absolute_uri(rest_password_url)}'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({'success': 'Password reset email sent'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
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
    permission_classes = [IsAuthenticated, IsStudent]

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
