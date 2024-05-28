from django.contrib import admin
from api.models import User, Profile, ContactMessage, BloodFormSubmission, File, Test
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import   Specialty, ContactInfo, RendezVous, Category, Faq


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


@admin.register(BloodFormSubmission)
class BloodFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'appointment_date')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('test', 'file', 'description')


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [FaqInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Faq)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("adresseLab", "telephoneLab", "emailLab")
    search_fields = ("adresseLab", "telephoneLab", "emailLab")


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ("appointmentID", "date", "prescription")
    search_fields = ("date",)
    list_filter = ("date",)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)