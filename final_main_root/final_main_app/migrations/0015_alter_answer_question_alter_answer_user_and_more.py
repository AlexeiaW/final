# Generated by Django 4.0.6 on 2023-01-19 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final_main_app', '0014_content_remove_answer_answer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='final_main_app.question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='final_main_app.appuser'),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='status',
            field=models.TextField(blank=True, max_length=256, null=True),
        ),
    ]
