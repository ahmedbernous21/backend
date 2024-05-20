# Generated by Django 5.0.4 on 2024-05-20 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_contactmessage_phone_contactmessage_sujet'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodFormSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('appointment_date', models.DateTimeField()),
                ('message', models.TextField()),
                ('prescription', models.FileField(blank=True, null=True, upload_to='prescriptions/')),
            ],
        ),
    ]
