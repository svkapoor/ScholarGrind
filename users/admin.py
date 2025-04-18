from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'student_type', 'institution', 'major', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Student Info', {
            'fields': ('student_type', 'institution', 'major', 'bio', 'study_points')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Student Info', {
            'fields': ('student_type', 'institution', 'major', 'bio', 'study_points')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
