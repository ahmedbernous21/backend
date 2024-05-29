from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def profile(self):
        profile = Profile.objects.get(user=self)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    bio = models.CharField(max_length=100)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    verified = models.BooleanField(default=False)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, default="N/A")
    sujet = models.CharField(max_length=100)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BloodFormSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    appointment_date = models.DateTimeField()
    message = models.TextField()
    prescription = models.FileField(upload_to="prescriptions/", default="default.png")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name 

class File(models.Model):
    test = models.ForeignKey(Test, related_name='files', on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='test_files/', default='test_files/ECBU.pdf')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.file.name

  


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/', )

    def __str__(self):
        return self.name

class Faq(models.Model):
    category = models.ForeignKey(Category, related_name='faqs', on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_text = models.TextField()

    def __str__(self):
        return self.question_text


class Specialty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='specialties/')

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    adresseLab = models.CharField(max_length=255)
    telephoneLab = models.CharField(max_length=15)
    emailLab = models.EmailField()

    def __str__(self):
        return self.adresseLab


class Appointment(models.Model):
    patient_name = models.CharField(max_length=255)
    test_name = models.CharField(max_length=255)
    apt_notes = models.TextField(blank=True, null=True)
    apt_date = models.DateField()
    apt_time = models.TimeField()
    apt_pres = models.FileField(upload_to='prescriptions/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['apt_date', 'apt_time']

    def __str__(self):
        return f"{self.patient_name} - {self.test_name} on {self.apt_date} at {self.apt_time}"
