from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
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


@admin.register(EducationGrade)
class EducationGradeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "education_stage", "get_country", "created")
    search_fields = ("name",)
    list_filter = ("education_stage__country", "education_stage")
    
    def get_country(self, obj):
        return obj.education_stage.country
    
    get_country.short_description = "Country"
    get_country.admin_order_field = "education_stage__country"
    
    class Media:
        js = ('admin/js/education_grade_filter.js',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "education_stage":
            kwargs["queryset"] = EducationStage.objects.order_by('country__name', 'name').select_related("country")
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
            kwargs["queryset"] = EducationGrade.objects.order_by('education_stage__country__name', 'education_stage__name', 'name').select_related("education_stage__country")
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
            kwargs["queryset"] = Semester.objects.order_by('education_grade__education_stage__country__name', 'education_grade__education_stage__name', 'education_grade__name', 'name').select_related("education_grade__education_stage__country")
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
        "get_test_link",
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

    def get_test_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>'.format(
                obj.test_link, "Test Link"
            )
        )

    get_test_link.short_description = "Test Link"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.order_by('name').select_related("subject__semester__education_grade__education_stage__country")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def render_change_form(self, request, context, *args, **kwargs):
        if 'course' in context['adminform'].form.fields:
            course_field = context['adminform'].form.fields['course']
            obj = context['original']
            if obj and obj.course and obj.course.subject:
                course_field.label_from_instance = lambda obj: f"{obj.course.subject.semester.education_grade.education_stage.country.name} - {obj.course.subject.semester.education_grade.education_stage.name} - {obj.course.subject.semester.education_grade.name} - {obj.course.subject.semester.name} - {obj.course.subject.name} - {obj.name}"
            else:
                course_field.label_from_instance = lambda obj: f"{obj.name}"
        return super().render_change_form(request, context, *args, **kwargs)

    def get_urls(self):
        """Extend admin with custom URL"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "generate-host-link/<int:lesson_id>/",
                self.admin_site.admin_view(self.generate_host_link),
                name="generate_host_link",
            ),
        ]
        return custom_urls + urls

    def video_room_button(self, obj):
        """Show button in admin list to generate host link"""
        url = reverse("admin:generate_host_link", args=[obj.id])
        return format_html(f'<a class="button" href="{url}">🎥 Generate Room</a>')
    video_room_button.short_description = "Video Room"

    def generate_host_link(self, request, lesson_id):
        """Custom admin action: generate host link + update lesson.video_link"""
        lesson = get_object_or_404(Lesson, pk=lesson_id)

        # Use lesson.id as roomID, and teacher name
        room_id = str(lesson.id)
        teacher_name = getattr(lesson.course, "teacher", None)
        teacher_name = teacher_name.first_name if teacher_name else "Teacher"

        # Build links
        base_url = request.build_absolute_uri(f"/courses/lesson/{lesson_id}/generate-host-link/")
        host_link = f"{base_url}?roomID={room_id}&role=Host&userName={teacher_name}"
        audience_link = f"{base_url}?roomID={room_id}&role=Audience"

        # Save audience link to lesson
        lesson.video_link = audience_link
        lesson.save(update_fields=["video_link"])

        # Show success message in admin
        self.message_user(request, f"✅ Host link generated: {host_link}")

        # Redirect back to the lesson changelist
        return redirect(request.META.get("HTTP_REFERER", "admin:index"))

