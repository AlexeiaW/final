# Generated by Django 4.0.6 on 2022-11-02 09:01

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('final_main_app', '0007_alter_answer_user_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=django_quill.fields.QuillField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=django_quill.fields.QuillField(),
        ),
    ]
