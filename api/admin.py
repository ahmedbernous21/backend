from django.contrib import admin
from api.models import User, Profile, ContactMessage


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ["verified"]
    list_display = ["user", "full_name", "verified"]


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "date_sent", "responded"]
    list_editable = ["responded"]
    search_fields = ["name", "email", "message"]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
