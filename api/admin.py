from django.contrib import admin
from api.models import User, Profile, ContactMessage, BloodFormSubmission
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ["verified"]
    list_display = ["user", "full_name", "verified"]


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "date_sent", "respond", "responded"]
    list_editable = ["responded"]
    search_fields = ["name", "email", "message"]

    def respond(self, obj):
        if not obj.responded:
            return format_html(
                '<a href="{}">Respond</a>',
                reverse("admin:send_response", args=[obj.id]),
            )
        return "Already Responded"

    respond.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "send-response/<int:message_id>/",
                self.send_response_view,
                name="send_response",
            ),
        ]
        return custom_urls + urls

    def send_response_view(self, request, message_id):
        message = get_object_or_404(ContactMessage, pk=message_id)
        if request.method == "POST":
            message.responded = True
            message.save()

            messages.success(request, "Response sent successfully!")
            return redirect(reverse("admin:api_contactmessage_changelist"))
        else:
            # Render the response form template
            context = {
                "message": message,
            }
            return render(request, "response_form.html", context)


class BloodFormSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "address",
        "phone",
        "appointment_date",
        "message",
        "prescription",
    )
    search_fields = ("first_name", "last_name", "email", "phone")
    list_filter = ("appointment_date",)
    readonly_fields = (
        "first_name",
        "last_name",
        "email",
        "address",
        "phone",
        "appointment_date",
        "message",
        "prescription",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(BloodFormSubmission, BloodFormSubmissionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
