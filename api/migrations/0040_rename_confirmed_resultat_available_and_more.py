# Generated by Django 5.0.4 on 2024-05-31 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_resultat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultat',
            old_name='confirmed',
            new_name='available',
        ),
        migrations.RemoveField(
            model_name='resultat',
            name='email',
        ),
        migrations.RemoveField(
            model_name='resultat',
            name='result_file',
        ),
        migrations.RemoveField(
            model_name='resultat',
            name='result_notes',
        ),
    ]