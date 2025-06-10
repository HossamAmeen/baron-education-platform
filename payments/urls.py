from django.urls import path
from payments.views import CoursePaymentView, PaymentCallbackView

urlpatterns = [
    path(
        "course/<int:course_id>/payment/",
        CoursePaymentView.as_view(),
        name="course-payment",
    ),
    path("paymob/callback/", PaymentCallbackView.as_view(), name="paymob-callback"),
]
