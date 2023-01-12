# Generated by Django 4.0.6 on 2023-01-11 14:33

from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('final_main_app', '0013_group_category_question_category_alter_question_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', django_quill.fields.QuillField()),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question',
        ),
        migrations.AddField(
            model_name='answer',
            name='content',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='final_main_app.content'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='content',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='final_main_app.content'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='story',
            name='content',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='final_main_app.content'),
        ),
    ]
