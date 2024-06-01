from django.contrib import admin
from api.models import User, Profile, ContactMessage, BloodFormSubmission, File, Test
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import   Specialty, ContactInfo,  Category, Faq, Appointment, Resultat
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, get_connection
from django.conf import settings


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
    actions = ['send_appointment_email']

    def display_file(self, obj):
        if obj.prescription:
            file_url = obj.prescription.url
            if file_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return format_html('<img src="{}" width="100" height="100" />', file_url)
            return format_html('<a href="{}" target="_blank">Download</a>', file_url)
        return "No file"
    display_file.short_description = 'File'
    
    def send_appointment_email(self, request, queryset):
        for submission in queryset:
            subject = 'Appointment Confirmation'
            message = f'Dear {submission.first_name} {submission.last_name},\n\n' \
                      f'This is a confirmation for your appointment on {submission.appointment_date}.\n\n' \
                      f'Thank you for choosing our service.'
            recipient_list = [submission.email]
            connection = get_connection()
            connection.ssl_context = settings.EMAIL_SSL_CONTEXT
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,recipient_list,connection=connection)

        self.message_user(request, f"Emails sent to {queryset.count()} users successfully.", messages.SUCCESS)

    send_appointment_email.short_description = 'Send appointment confirmation email to selected users'


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


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'test_name', 'apt_date','created_at')
    search_fields = ('patient_name', 'test_name', 'apt_notes')
    ordering = ('-created_at',)

@receiver(post_save, sender=User)
def create_user_result(sender, instance, created, **kwargs):
    if created:
        Resultat.objects.create(user=instance)

@admin.register(Resultat)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'available')
    search_fields = ('user', 'created_at')


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)