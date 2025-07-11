from rest_framework.response import Response
from rest_framework.views import APIView
from payments.models import Transaction
from rest_framework import status
from course.models import Course
from rest_framework.permissions import IsAuthenticated
from payments.services.paymob_payment_service import PaymobPaymentService
from course.models import StudentCourse
from django.db import transaction
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
import logging

from shared.permisions import IsStudent
logger = logging.getLogger("payments")


class CoursePaymentView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    @transaction.atomic
    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Payment successful",
                response={
                    "data": {
                        "iframe_url": "https://example.com/iframe_url"
                    }
                },
                examples=[
                    OpenApiExample(
                        "Payment successful",
                        value={
                            "data": {
                                "iframe_url": "https://example.com/iframe_url"
                            }
                        },
                    )
                ],
            )
        },
    )
    def post(self, request, course_id):
        course = Course.objects.filter(id=course_id).first()
        if not course:
            return Response(
                {"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )

        transaction = Transaction.objects.filter(
            user=request.user, student_courses__course=course
        ).first()
        if transaction:
            if transaction.status == Transaction.TransactionStatus.PAID:
                return Response(
                    {
                        "message": "You already paid for this course",
                        "data": {"transaction_id": transaction.id},
                    },
                    status=status.HTTP_200_OK,
                )
            payment_service = PaymobPaymentService()
            iframe_url = payment_service.get_iframe_url(transaction.client_secret)
            return Response(
                {"data": {"iframe_url": iframe_url}}, status=status.HTTP_200_OK
            )

        else:
            transaction = Transaction.objects.create(
                status="pending", user=request.user, amount=course.price
            )
            StudentCourse.objects.create(
                student_id=request.user.id, course=course, transaction=transaction
            )
        # Generate Paymob payment link
        payment_service = PaymobPaymentService()
        try:
            status_code, iframe_url = payment_service.create_paymob_intention(
                amount=course.price,
                customer=request.user,
                course=course,
                reference_id=transaction.id,
                transaction=transaction,
            )
        except Exception as e:
            logger.error("Error creating Paymob intention: %s", e)
            return Response(
                {"message": "Error creating Paymob intention"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"data": {"iframe_url": iframe_url}}, status=status_code)


class PaymentCallbackView(APIView):
    def post(self, request):
        paymob_transaction_id = request.data.get("obj", {}).get("id")
        logger.info("Payment callback request data: %s", request.data)

        transaction_id = (
            request.data.get("obj", {})
            .get("order", {})
            .get("merchant_order_id", " : ")
            .split(":")[1]
        )
        payment_status = (
            request.data.get("obj", {}).get("order", {}).get("payment_status", "")
        )
        try:
            transaction = Transaction.objects.get(id=int(transaction_id))
        except Transaction.DoesNotExist:
            logger.warning("Transaction not found: %s", transaction_id)
            return Response(
                {"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if payment_status == "PAID":
            transaction.status = "paid"
            transaction.gateway_transaction_id = paymob_transaction_id
            transaction.save()
            logger.info("Payment successful: %s", transaction_id)
            return Response({"message": "Payment successful"})
        else:
            transaction.status = "failed"
            transaction.save()
            logger.info("Payment failed: %s", transaction_id)
            return Response(
                {"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST
            )
