import django_filters

from .models import Subject


class SubjectFilter(django_filters.FilterSet):
    semester = django_filters.CharFilter(field_name="semester", lookup_expr="exact")
    grade = django_filters.CharFilter(
        field_name="semester__education_grade", lookup_expr="exact"
    )
    stage = django_filters.CharFilter(
        field_name="semester__education_grade__education_stage", lookup_expr="exact"
    )
    country = django_filters.CharFilter(
        field_name="semester__education_grade__education_stage__country",
        lookup_expr="exact",
    )
    is_tahsili = django_filters.BooleanFilter(field_name="is_tahsili")
    is_kamiy = django_filters.BooleanFilter(field_name="is_kamiy")

    class Meta:
        model = Subject
        fields = ["semester", "grade", "stage", "country", "is_tahsili", "is_kamiy"]
