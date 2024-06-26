# Generated by Django 5.0.4 on 2024-05-26 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_category_remove_faq_answer_remove_faq_faqid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='category_images/')),
            ],
        ),
        migrations.AlterField(
            model_name='faq',
            name='answer_text',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='faq',
            name='question_text',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='faq',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to='api.faqcategory'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
