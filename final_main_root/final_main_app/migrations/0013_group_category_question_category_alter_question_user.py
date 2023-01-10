# Generated by Django 4.0.6 on 2023-01-10 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final_main_app', '0012_rename_interest_appuser_interests'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_groups', to='final_main_app.category'),
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_questions', to='final_main_app.category'),
        ),
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appuser_questions', to='final_main_app.appuser'),
        ),
    ]
