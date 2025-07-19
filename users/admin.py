from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, make_password

from users.models import Student, User


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "password-field"}),
        required=False,
        help_text="Leave empty to keep the current password.",
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "password-field"}),
        required=False,
        help_text="Leave empty to keep the current password.",
    )

    class Meta:
        model = User
        exclude = (
            "is_superuser",
            "is_staff",
            "role",
            "last_login",
            "groups",
            "user_permissions",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.pop("password_confirmation")
        if password:
            if not password_confirmation:
                raise forms.ValidationError("Password confirmation is required.")
            if password != password_confirmation:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "phone", "parent_phone")
    search_fields = ("first_name", "last_name", "phone", "parent_phone")
    list_filter = ("phone", "parent_phone")
    exclude = (
        "is_superuser",
        "is_staff",
        "role",
        "last_login",
        "groups",
        "user_permissions",
    )
    form = UserForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "parent_phone",
                    "email",
                    "gender",
                    "password",
                    "password_confirmation",
                )
            },
        ),
    )


class AdminForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=False,
        help_text='Raw passwords are not stored, so there is no way to see this user\'s password, but you can change the password using <a href="../password/">this form</a>.',
    )
    password_confirmation = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        required=False,
        help_text="Enter the same password as above, for verification.",
    )

    class Meta:
        model = User
        exclude = (
            "last_login",
            "groups",
            "user_permissions",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.pop("password_confirmation")

        if password:
            if password != password_confirmation:
                raise forms.ValidationError("Passwords do not match.")
            cleaned_data["password"] = make_password(password)
        return cleaned_data


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "phone", "email", "role")
    search_fields = ("phone", "email", "role")
    list_filter = ("phone", "email", "role")
    form = AdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "email",
                    "gender",
                    "role",
                    "is_staff",
                    "is_superuser",
                    "password",
                    "password_confirmation",
                )
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(role="student")


admin.site.unregister(Group)
