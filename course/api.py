from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from course.filters import SubjectFilter
from course.models import (
    Country,
    Course,
    EducationStage,
    Group,
    Lesson,
    Semester,
    StudentCourse,
    Subject,
)
from course.serializers import (
    CountrySerializer,
    CourseSerializer,
    EducationStageSerializer,
    GroupSerializer,
    LessonSerializer,
    ListCourseSerializer,
    RetrieveCourseSerializer,
    SemesterSerializer,
    SubjectSerializer,
)
from payments.models import Transaction
from payments.services.paymob_payment_service import PaymobPaymentService


class CountryListAPIView(ListAPIView):
    queryset = Country.objects.prefetch_related(
        "educationstage_set__educationgrade_set__semester_set"
    ).order_by("-id")
    serializer_class = CountrySerializer


class EducationStageViewSet(ModelViewSet):
    schema = None
    queryset = EducationStage.objects.prefetch_related(
        "educationgrade_set__semester_set"
    ).order_by("-id")
    serializer_class = EducationStageSerializer


class SemesterViewSet(ModelViewSet):
    schema = None
    queryset = Semester.objects.order_by("-id")
    serializer_class = SemesterSerializer


class GroupViewSet(ModelViewSet):
    schema = None
    queryset = Group.objects.order_by("-id")
    serializer_class = GroupSerializer


class CourseViweSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Course.objects.order_by("-id")

    def get_serializer_class(self):
        if self.action == "list":
            return ListCourseSerializer
        if self.action == "retrieve":
            return RetrieveCourseSerializer
        return CourseSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            self.queryset.filter(student_courses__student=self.request.user)
        return self.queryset


class LessonViewSet(ModelViewSet):
    schema = None
    queryset = Lesson.objects.order_by("-id")
    serializer_class = LessonSerializer


class SubjectViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Subject.objects.prefetch_related(
        Prefetch(
            "course_set",
            queryset=Course.objects.filter(available=True)[:1],
            to_attr="available_courses",
        )
    ).order_by("-id")

    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter


class CoursePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = Course.objects.filter(id=course_id).first()
        if not course:
            return Response(
                {"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )

        transaction = Transaction.objects.filter(
            user=request.user,
            student_courses__course=course
        ).first()
        if transaction:
            if transaction.status == Transaction.TransactionStatus.PAID:
                return Response(
                    {"message": "You already paid for this course",
                    "data": {"transaction_id": transaction.id}},
                    status=status.HTTP_200_OK,
                )
            payment_service = PaymobPaymentService()
            iframe_url = payment_service.get_iframe_url(transaction.client_secret)
            return Response(
                {"data": {"iframe_url": iframe_url}}, status=status.HTTP_200_OK)
                
        else:
            transaction = Transaction.objects.create(
                status="pending", user=request.user, amount=course.price
            )
            StudentCourse.objects.create(
                student_id=request.user.id, course=course, transaction=transaction
            )
        # Generate Paymob payment link
        payment_service = PaymobPaymentService()
        status_code,iframe_url = payment_service.create_paymob_intention(
            amount=course.price, customer=request.user, course=course, reference_id=transaction.id, transaction=transaction)

        return Response(
            {"data": {"iframe_url": iframe_url}}, status=status_code
        )


class PaymentCallbackView(APIView):
    def post(self, request):
        paymob_transaction_id = request.data.get("paymob_transaction_id")
        transaction_id = request.data.get("transaction_id")
        status = request.data.get("status")

        try:
            transaction = Transaction.objects.get(
                id=transaction_id, gateway_transaction_id=paymob_transaction_id
            )
        except Transaction.DoesNotExist:
            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if status == "paid":
            transaction.status = "paid"
            transaction.save()
            return Response(
                {"message": f"Payment successful for {transaction.payment_for}!"}
            )
        else:
            transaction.status = "failed"
            transaction.save()
            return Response(
                {"message": "Payment failed"},
                status=status.HTTP_400_BAD_REQUEST
            )
