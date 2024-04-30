from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        first_name = models.CharField(max_length=255)
        last_name = models.CharField(max_length=255)
        bio =  models.CharField(max_length=255)
        avatar = models.ImageField(default='default.png', upload_to='avatars/', null=True, blank=True)
        verified = models.BooleanField(default=False)

        def __str__(self):
            return self.first_name


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)