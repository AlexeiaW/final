# Generated by Django 4.0.6 on 2023-02-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_main_app', '0002_badge'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='icon',
            field=models.FileField(default='', upload_to='badge_icons/'),
            preserve_default=False,
        ),
    ]
