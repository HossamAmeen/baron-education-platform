from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import User, Student
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password-field'}), required=False)

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'role', 'last_login', 'groups', 'user_permissions')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'parent_phone')
    search_fields = ('phone', 'parent_phone')
    list_filter = ('phone', 'parent_phone')
    exclude = ('is_superuser', 'is_staff', 'role', 'last_login', 'groups', 'user_permissions')
    form = UserForm

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email', 'role')
    search_fields = ('phone', 'email', 'role')
    list_filter = ('phone', 'email', 'role')

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)