from django.contrib import admin

from configuration.models import Configuration, ContactUs, Review, Slider


# Register your models here.
class SliderAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "image")
    search_fields = ("link",)
    list_filter = ("link",)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "phone", "subject")
    search_fields = ("phone",)
    list_filter = ("phone",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rate", "description", "ordering")
    search_fields = ("name",)
    list_filter = ("rate",)


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "eg_number",
        "ksa_number",
        "eg_adderss",
        "ksa_adderss",
        "email",
        "about_us",
        "our_vision",
        "our_mission",
        "student_counter",
        "teacher_counter",
        "partner_counter",
        "meta",
        "twitter",
        "linkedin",
        "googel",
        "footer_description",
    )
    search_fields = ("email", "twitter", "linkedin", "googel", "meta")
    list_filter = ("email",)


admin.site.register(Slider, SliderAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
