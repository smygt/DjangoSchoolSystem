# Generated by Django 2.2.7 on 2019-11-11 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainProject', '0003_remove_lecture_asdrse_materials'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcement',
            old_name='announcements',
            new_name='lecture',
        ),
    ]