# Generated by Django 3.0 on 2022-07-14 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_main_app', '0004_appuser_alter_image_user_alter_userfriends_friend_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userfriends',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
