# Generated by Django 5.0.7 on 2024-08-22 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_category_name_alter_tags_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body_text',
            field=models.TextField(default=1, editable=False),
            preserve_default=False,
        ),
    ]