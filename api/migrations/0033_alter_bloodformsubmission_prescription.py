# Generated by Django 5.0.4 on 2024-05-28 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_alter_bloodformsubmission_prescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodformsubmission',
            name='prescription',
            field=models.FileField(default='default.png', upload_to='prescriptions/'),
        ),
    ]
