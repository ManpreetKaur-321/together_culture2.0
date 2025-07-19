from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new user
            if obj.is_superuser:
                obj.role = User.ADMIN
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)
