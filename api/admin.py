from django.contrib import admin
from api.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ProfileAdmin(admin.ModelAdmin):
        list_editable = ['verified', 'full_name']
        list_display = ('user', 'full_name', 'verified')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)