from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User, Employer

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person_name', 'email', 'phone_number', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('company_name', 'contact_person_name', 'email')
    readonly_fields = ('created_at',)

admin.site.register(User, UserAdmin)
admin.site.register(Employer, EmployerAdmin)
