# Generated by Django 4.0.6 on 2022-10-18 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final_main_app', '0009_appuser_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ManyToManyField(to='final_main_app.appuser')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='final_main_app.group')),
            ],
        ),
    ]
