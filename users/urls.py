from rest_framework.routers import DefaultRouter
from django.urls import path
from users.api import (AdminViewSet, ManagerViewSet, StudentViewSet,
                       TeacherViewSet, StudentCourseListView)

router = DefaultRouter()
router.register(r'admins', AdminViewSet, basename="admins")
router.register(r'teachers', TeacherViewSet, basename="teachers")
router.register(r'students', StudentViewSet, basename="students")
router.register(r'managers', ManagerViewSet, basename="managers")
urlpatterns = router.urls

urlpatterns = [
    path('student/courses/', StudentCourseListView.as_view(), name='student-course-list'),
]
