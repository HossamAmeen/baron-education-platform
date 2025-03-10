from django.contrib import admin

from .models import Country, EducationGrade, EducationStage, Semester, Subject


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name',)
    list_filter = ('code',)

class EducationStageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)

class EducationGradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'education_stage')
    search_fields = ('name',)
    list_filter = ('education_stage',)

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'education_grade')
    search_fields = ('name',)
    list_filter = ('education_grade',)

# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'semester', 'grade', 'stage', 'country')
#     search_fields = ('name',)
#     list_filter = ('semester', 'grade', 'stage', 'country')

# Register your models here.
admin.site.register(Country, CountryAdmin)
admin.site.register(EducationStage, EducationStageAdmin)
admin.site.register(EducationGrade, EducationGradeAdmin)
admin.site.register(Semester, SemesterAdmin)
# admin.site.register(Subject, SubjectAdmin)
