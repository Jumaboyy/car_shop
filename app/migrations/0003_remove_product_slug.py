# Generated by Django 5.0.3 on 2024-05-13 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]