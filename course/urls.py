from django.urls import path
from rest_framework.routers import DefaultRouter

from course.api import (
    CountryListAPIView,
    CourseViweSet,
    EducationStageViewSet,
    GroupViewSet,
    LessonViewSet,
    SemesterViewSet,
    SubjectViewSet,
)
from course.views import VideoRoomView

router = DefaultRouter()
router.register(
    r"education-stages", EducationStageViewSet, basename="education-stations"
)
router.register(r"semesters", SemesterViewSet, basename="semesters")
router.register(r"groups", GroupViewSet, basename="groups")
router.register(r"courses", CourseViweSet, basename="courses")
router.register(r"lessons", LessonViewSet, basename="lessons")
router.register(r"subjects", SubjectViewSet, basename="subjects")
urlpatterns = router.urls

urlpatterns += [
    path("countries/", CountryListAPIView.as_view(), name="countries"),
    path("lesson/<int:lesson_id>/generate-host-link/", VideoRoomView.as_view(), name="generate-host-link"),
]
