from rest_framework.routers import DefaultRouter

from course.api import (CityViewSet, CountryViewSet, CourseViweSet,
                        GroupViewSet, LessonViewSet, SemesterViewSet, EducationStageViewSet,
                        SubjectViewSet)

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename="countries")
router.register(r'cities', CityViewSet, basename="cities")
router.register(r'education-stages', EducationStageViewSet, basename="education-stations")
router.register(r'semesters', SemesterViewSet, basename="semesters")
router.register(r'groups', GroupViewSet, basename="groups")
router.register(r'courses', CourseViweSet, basename="courses")
router.register(r'lessons', LessonViewSet, basename="lessons")
router.register(r'subjects', SubjectViewSet, basename="subjects")
urlpatterns = router.urls
