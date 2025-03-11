from django.contrib import admin
from auth.models import PasswordReset

class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created')
    search_fields = ('email',)
    list_filter = ('created',)

admin.site.register(PasswordReset, PasswordResetAdmin)
