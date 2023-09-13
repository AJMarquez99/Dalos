from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import CustomUser

# Register your models here.
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", 
                                widget=forms.PasswordInput,
                                help_text="""<ul>
                                <li>Password must be at least 8 characters long.</li>
                                </ul>""")
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )



    class Meta:
        model = CustomUser
        fields = ["email", "email2", "f_name", "l_name", "date_of_birth"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ["email", "email2", "f_name", "l_name", "date_of_birth", "password", "is_active", "is_admin"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "email2", "f_name", "l_name", "date_of_birth", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal Info", {"fields": ["f_name", "l_name", "email2", "date_of_birth"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "email2", "f_name", "l_name", "date_of_birth", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)