# Generated by Django 4.0.6 on 2023-01-04 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_main_app', '0008_alter_answer_answer_alter_question_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]