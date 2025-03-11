from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import User, Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'parent_phone', 'address')
    search_fields = ('phone', 'parent_phone')
    list_filter = ('phone', 'parent_phone')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email', 'role')
    search_fields = ('phone', 'email', 'role')
    list_filter = ('phone', 'email', 'role')

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)