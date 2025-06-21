from django.contrib import admin

from .models import Country, Course, EducationGrade, EducationStage, Semester, Subject


class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")
    search_fields = ("name",)
    list_filter = ("code",)


class EducationStageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country")
    search_fields = ("name",)
    list_filter = ("country",)


class EducationGradeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "education_stage", "get_country")
    search_fields = ("name",)
    list_filter = ("education_stage", "education_stage__country")

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
        "education_grade__education_stage",
    )

    def get_education_stage(self, obj):
        return obj.education_grade.education_stage

    get_education_stage.short_description = "Education Stage"
    get_education_stage.admin_order_field = (
        "education_grade__education_stage"  # Allows sorting by education stage
    )

    def get_country(self, obj):
        return obj.education_grade.education_stage.country

    get_country.short_description = "Country"
    get_country.admin_order_field = (
        "education_grade__education_stage__country"  # Allows sorting by country
    )


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


admin.site.register(Country, CountryAdmin)
admin.site.register(EducationStage, EducationStageAdmin)
admin.site.register(EducationGrade, EducationGradeAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Course, CourseAdmin)
