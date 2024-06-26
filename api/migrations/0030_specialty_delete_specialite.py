# Generated by Django 5.0.4 on 2024-05-26 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_category_alter_faq_question_text_alter_faq_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='specialties/')),
            ],
        ),
        migrations.DeleteModel(
            name='Specialite',
        ),
    ]
