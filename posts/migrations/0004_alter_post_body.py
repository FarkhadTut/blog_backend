# Generated by Django 5.0.7 on 2024-08-16 09:23

import django_quill.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=django_quill.fields.QuillField(),
        ),
    ]
