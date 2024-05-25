from django.contrib import admin
from api.models import User, Profile, ContactMessage, BloodFormSubmission
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import File, Test, Categorie, FAQ, Specialite, ContactInfo, RendezVous


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

    def display_prescription(self, obj):
        if obj.prescription:
            return '<img src="%s" width="100" />' % obj.prescription.url
        else:
            return "(No prescription)"

    display_prescription.allow_tags = True


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("fileID", "filePath")
    search_fields = ("filePath",)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("testID", "testName")
    search_fields = ("testName",)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("categoryID", "categoryName", "description")
    search_fields = ("categoryName",)
    list_filter = ("categoryName",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("faqID", "question", "answer", "category")
    search_fields = ("question", "answer")
    list_filter = ("category",)


@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ("specialtyID", "name", "description")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("adresseLab", "telephoneLab", "emailLab")
    search_fields = ("adresseLab", "telephoneLab", "emailLab")


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ("appointmentID", "date", "prescription")
    search_fields = ("date",)
    list_filter = ("date",)


admin.site.register(BloodFormSubmission, BloodFormSubmissionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
