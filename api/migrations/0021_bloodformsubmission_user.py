# api/migrations/0021_bloodformsubmission_user.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_rename_coordonnees_contactinfo'),  # Adjust to your previous migration
    ]

    operations = [
        migrations.AddField(
            model_name='bloodformsubmission',
            name='user',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=models.CASCADE,
                to='api.User'  # Adjust to your user model path
            ),
        ),
    ]
