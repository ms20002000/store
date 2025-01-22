from django.contrib import admin
from account.models import CustomUser

admin.site.site_header = "Store Admin Panel"
admin.site.site_title = "Store Administration"
admin.site.index_title = "Welcome to the Store Admin Panel"

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('phone_number', 'first_name', 'last_name', 'email')
    # ordering = ('phone_number',)
    # fieldsets = (
    #     (None, {'fields': ('phone_number', 'password')}),
    #     ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'profile_picture', 'address')}),
    #     ('Role and Permissions', {'fields': ('role', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    #     ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    # )
    readonly_fields = ('created_at', 'updated_at', 'last_login')
