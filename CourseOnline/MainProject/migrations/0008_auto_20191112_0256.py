# Generated by Django 2.2.7 on 2019-11-11 23:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MainProject', '0007_auto_20191112_0235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]