# Generated by Django 5.0.4 on 2024-05-28 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_alter_bloodformsubmission_prescription_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodformsubmission',
            name='prescription',
            field=models.ImageField(default='default.png', upload_to='prescriptions/'),
        ),
    ]
