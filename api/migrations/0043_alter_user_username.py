# Generated by Django 5.0.4 on 2024-05-31 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_alter_resultat_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
