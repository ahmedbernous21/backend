# Generated by Django 5.0.4 on 2024-05-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_faqcategory_alter_faq_answer_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqcategory',
            name='html_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question_text',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='faqcategory',
            name='image',
            field=models.ImageField(upload_to='category_images'),
        ),
    ]
