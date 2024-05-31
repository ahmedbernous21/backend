# Generated by Django 5.0.4 on 2024-05-31 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
