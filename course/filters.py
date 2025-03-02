import django_filters
from .models import Subject

class SubjectFilter(django_filters.FilterSet):
    semester = django_filters.CharFilter(field_name='semester', lookup_expr='exact')
    grade = django_filters.CharFilter(field_name='semester__education_grade', lookup_expr='exact')
    stage = django_filters.CharFilter(field_name='semester__education_grade__education_stage', lookup_expr='exact')
    country = django_filters.CharFilter(field_name='semester__education_grade__education_stage__country', lookup_expr='exact')

    class Meta:
        model = Subject
        fields = ['semester', 'grade', 'stage', 'country']
