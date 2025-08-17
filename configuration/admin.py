from django.contrib import admin

from configuration.models import Configuration, ContactUs, Review, Slider


# Register your models here.
class SliderAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "image")
    search_fields = ("link",)
    list_filter = ("link",)
    list_per_page = 50


class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone",
        "subject",
        "get_description",
        "created",
    )
    search_fields = ("phone",)
    list_filter = ("phone", "subject", "created")

    list_per_page = 50


    def get_description(self, obj):
        return obj.description[:5]
    get_description.short_description = "short description"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rate", "description", "ordering")
    search_fields = ("name",)
    list_filter = ("rate",)
    list_per_page = 50


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "eg_number",
        "ksa_number",
        "eg_adderss",
        "ksa_adderss",
        "email",
        "student_counter",
        "teacher_counter",
        "partner_counter",
        "twitter",
        "linkedin",
        "googel",
        "whatsapp_number",
    )
    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Slider, SliderAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
