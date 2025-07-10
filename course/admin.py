from django.contrib import admin

from .models import Country, Course, EducationGrade, EducationStage, Lesson, Semester, StudentCourse, Subject
from django.utils.html import format_html
from django.urls import reverse


class EducationStageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country")
    search_fields = ("name",)
    list_filter = ("country",)


class EducationGradeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "education_stage", "get_country")
    search_fields = ("name",)
    list_filter = ("education_stage__country",)

    def get_country(self, obj):
        return obj.education_stage.country

    get_country.short_description = "Country"
    get_country.admin_order_field = (
        "education_stage__country"  # Allows sorting by country
    )


class SemesterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "education_grade",
        "get_education_stage",
        "get_country",
    )
    search_fields = ("name",)
    list_filter = (
        "education_grade__education_stage__country",
        "education_grade",
    )

    def get_education_stage(self, obj):
        return obj.education_grade.education_stage

    get_education_stage.short_description = "Education Stage"

    def get_country(self, obj):
        return obj.education_grade.education_stage.country

    get_country.short_description = "Country"


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "available",
        "image",
        "semester",
        "get_education_grade",
        "get_education_stage",
        "get_country",
    )
    search_fields = ("name",)
    list_filter = ("available",)

    def get_education_grade(self, obj):
        return obj.semester.education_grade

    get_education_grade.short_description = "Education Grade"
    get_education_grade.admin_order_field = (
        "semester__education_grade"  # Allows sorting by education grade
    )

    def get_education_stage(self, obj):
        return obj.semester.education_grade.education_stage

    get_education_stage.short_description = "Education Stage"
    get_education_stage.admin_order_field = "semester__education_grade__education_stage"  # Allows sorting by education stage

    def get_country(self, obj):
        return obj.semester.education_grade.education_stage.country

    get_country.short_description = "Country"
    get_country.admin_order_field = "semester__education_grade__education_stage__country"  # Allows sorting by country


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "available",
        "start_date",
        "hours_count",
        "duration",
    )
    search_fields = ("name",)
    list_filter = ("available",)

@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student_link",
        "course_link",
        "transaction_link",
    )
    search_fields = ("student", "course")
    list_filter = ("student", "course", "transaction")
    page_size = 10
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("student", "course", "transaction")

    def student_link(self, obj):
        return format_html('<a href="{}">{}</a>'.format(
            reverse('admin:users_student_change', args=(obj.student.pk,)),
            obj.student
        ))

    student_link.short_description = 'Student'

    def course_link(self, obj):
        return format_html('<a href="{}">{}</a>'.format(
            reverse('admin:course_course_change', args=(obj.course.pk,)),
            obj.course
        ))

    course_link.short_description = 'Course'

    def transaction_link(self, obj):
        return format_html('<a href="{}">{}</a>'.format(
            reverse('admin:payments_transaction_change', args=(obj.transaction.pk,)),
            obj.transaction
        ))

    transaction_link.short_description = 'Transaction_info'

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")
    search_fields = ("name",)
    list_filter = ("code",)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "date",
        "time",
        "explanation_file",
        "test_link",
        "video_link",
        "course",
    )
    search_fields = ("title",)
    list_filter = ("course",)
    page_size = 10
    list_per_page = 10

admin.site.register(EducationStage, EducationStageAdmin)
admin.site.register(EducationGrade, EducationGradeAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Course, CourseAdmin)
