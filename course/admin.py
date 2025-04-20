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
    list_display = ('id', 'name', 'education_stage', 'education_stage__country')
    search_fields = ('name',)
    list_filter = ('education_stage', 'education_stage__country')

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'education_grade', 'education_grade__education_stage', 'education_grade__education_stage__country')
    search_fields = ('name',)
    list_filter = ('education_grade', 'education_grade__education_stage', 'education_grade__education_stage__country')

# Register your models here.
admin.site.register(Country, CountryAdmin)
admin.site.register(EducationStage, EducationStageAdmin)
admin.site.register(EducationGrade, EducationGradeAdmin)
admin.site.register(Semester, SemesterAdmin)
# admin.site.register(Subject, SubjectAdmin)
