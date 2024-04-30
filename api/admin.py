from django.contrib import admin
from api.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('first_name', 'last_name', 'email', 'is_active','date_joined')
    search_fields = ('first_name', 'last_name','email')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ProfileAdmin(admin.ModelAdmin):
        list_editable = ['verified', 'first_name', 'last_name']
        list_display = ('user', 'first_name', 'last_name', 'verified')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)