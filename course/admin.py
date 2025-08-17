from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from payments.models import Transaction

from .models import (
    Country,
    Course,
    EducationGrade,
    EducationStage,
    Lesson,
    Semester,
    StudentCourse,
    Subject,
)

from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "created")
    search_fields = ("name",)
    list_filter = ("code",)

@admin.register(EducationStage)
class EducationStageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "created")
    search_fields = ("name",)
    list_filter = ("country",)


class EducationGradeForm(forms.ModelForm):
    class Meta:
        model = EducationGrade
        fields = '__all__'


@admin.register(EducationGrade)
class EducationGradeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "education_stage", "get_country", "created")
    search_fields = ("name",)
    list_filter = ("education_stage__country", "education_stage")
    # form = EducationGradeForm
    
    def get_country(self, obj):
        return obj.education_stage.country
    
    get_country.short_description = "Country"
    get_country.admin_order_field = "education_stage__country"
    
    class Media:
        js = ('admin/js/education_grade_filter.js',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "education_stage":
            kwargs["queryset"] = EducationStage.objects.order_by('name').select_related("country")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def render_change_form(self, request, context, *args, **kwargs):
        if 'education_stage' in context['adminform'].form.fields:
            education_stage_field = context['adminform'].form.fields['education_stage']
            education_stage_field.label_from_instance = lambda obj: f"{obj.country.name} - {obj.name}"
        return super().render_change_form(request, context, *args, **kwargs)
    
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "education_grade",
        "get_education_stage",
        "get_country",
        "created",
    )
    search_fields = ("name",)
    list_filter = (
        "education_grade__education_stage__country",
        "education_grade__education_stage",
        "education_grade",
    )

    def get_education_stage(self, obj):
        return obj.education_grade.education_stage

    get_education_stage.short_description = "Education Stage"

    def get_country(self, obj):
        return obj.education_grade.education_stage.country

    get_country.short_description = "Country"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "education_grade":
            kwargs["queryset"] = EducationGrade.objects.order_by('name').select_related("education_stage__country")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def render_change_form(self, request, context, *args, **kwargs):
        if 'education_grade' in context['adminform'].form.fields:
            education_grade_field = context['adminform'].form.fields['education_grade']
            education_grade_field.label_from_instance = lambda obj: f"{obj.education_stage.country.name} - {obj.education_stage.name} - {obj.name}"
        return super().render_change_form(request, context, *args, **kwargs)

@admin.register(Subject)
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
        "created",
    )
    search_fields = ("name",)
    list_filter = ("available", "semester__education_grade__education_stage__country", "semester__education_grade__education_stage", "semester__education_grade", "semester")

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "semester":
            kwargs["queryset"] = Semester.objects.order_by('name').select_related("education_grade__education_stage__country")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def render_change_form(self, request, context, *args, **kwargs):
        if 'semester' in context['adminform'].form.fields:
            semester_field = context['adminform'].form.fields['semester']
            semester_field.label_from_instance = lambda obj: f"{obj.education_grade.education_stage.country.name} - {obj.education_grade.education_stage.name} - {obj.education_grade.name} - {obj.name}"
        return super().render_change_form(request, context, *args, **kwargs)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "available",
        "start_date",
        "hours_count",
        "duration",
        "subject",
        "created",
    )
    search_fields = ("name",)
    list_filter = ("available", "subject")
    page_size = 10
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("subject")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            kwargs["queryset"] = Subject.objects.order_by('name').select_related("semester__education_grade__education_stage__country")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def render_change_form(self, request, context, *args, **kwargs):
        if 'subject' in context['adminform'].form.fields:
            subject_field = context['adminform'].form.fields['subject']
            subject_field.label_from_instance = lambda obj: f"{obj.semester.education_grade.education_stage.country.name} - {obj.semester.education_grade.education_stage.name} - {obj.semester.education_grade.name} - {obj.semester.name} - {obj.name}"
        return super().render_change_form(request, context, *args, **kwargs)

@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student_link",
        "course_link",
        "transaction_link",
        "transaction__status",
        "transaction__modified",
    )
    search_fields = ("student", "course")
    list_filter = ("student", "course", "transaction__status")
    page_size = 10
    list_per_page = 10

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("student", "course", "transaction")
        )

    def student_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>'.format(
                reverse("admin:users_student_change", args=(obj.student.pk,)),
                obj.student,
            )
        )

    student_link.short_description = "Student"

    def course_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>'.format(
                reverse("admin:course_course_change", args=(obj.course.pk,)), obj.course
            )
        )

    course_link.short_description = "Course"

    def transaction_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>'.format(
                reverse(
                    "admin:payments_transaction_change", args=(obj.transaction.pk,)
                ),
                obj.transaction,
            )
        )

    transaction_link.short_description = "Transaction_info"

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        if obj and obj.transaction.status == Transaction.TransactionStatus.PAID:
            return False
        return True

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
        "course__subject",
        "video_room_button",
        "created",
    )
    search_fields = ("title",)
    list_filter = ("course", "course__subject")
    page_size = 100
    list_per_page = 100

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("course", "course__subject")

    def course__subject(self, obj):
        if obj.course and obj.course.subject:
            return obj.course.subject.name
        return "N/A"

    course__subject.short_description = "Subject"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.order_by('name').select_related("subject__semester__education_grade__education_stage__country")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def render_change_form(self, request, context, *args, **kwargs):
        if 'course' in context['adminform'].form.fields:
            course_field = context['adminform'].form.fields['course']
            course_field.label_from_instance = lambda obj: f"{obj.subject.semester.education_grade.education_stage.country.name} - {obj.subject.semester.education_grade.education_stage.name} - {obj.subject.semester.education_grade.name} - {obj.subject.semester.name} - {obj.subject.name} - {obj.name}"
        return super().render_change_form(request, context, *args, **kwargs)

    def video_room_button(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">Open Video Room</a>',
            reverse('video-room', args=[obj.id])
        )
    video_room_button.short_description = "Video Room"
    video_room_button.allow_tags = True
