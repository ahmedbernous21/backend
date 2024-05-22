from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    appointment_date = models.DateTimeField()
    message = models.TextField()
    prescription = models.FileField(upload_to="prescriptions/", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class File(models.Model):
    fileID = models.AutoField(primary_key=True)
    filePath = models.CharField(max_length=255)

    def __str__(self):
        return self.filePath


class Test(models.Model):
    testID = models.AutoField(primary_key=True)
    testName = models.CharField(max_length=255)

    def __str__(self):
        return self.testName


class Categorie(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.categoryName


class FAQ(models.Model):
    faqID = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Specialite(models.Model):
    specialtyID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Coordonnees(models.Model):
    adresseLab = models.CharField(max_length=255)
    telephoneLab = models.CharField(max_length=15)
    emailLab = models.EmailField()

    def __str__(self):
        return self.adresseLab


class RendezVous(models.Model):
    appointmentID = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    prescription = models.ImageField(upload_to="prescriptions/")

    def __str__(self):
        return f"Appointment on {self.date}"

    class Meta:
        verbose_name_plural = "RendezVous"
