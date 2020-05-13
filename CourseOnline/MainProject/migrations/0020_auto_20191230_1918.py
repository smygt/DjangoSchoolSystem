# Generated by Django 3.0.1 on 2019-12-30 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MainProject', '0019_auto_20191224_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, null=True)),
                ('content', models.CharField(max_length=1000, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('doc_file', models.FileField(upload_to='documents/%Y/%m/%d')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lecture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MainProject.Lecture')),
            ],
        ),
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('doc_file', models.FileField(null=True, upload_to='documents/%Y/%m/%d')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lecture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MainProject.Lecture')),
            ],
        ),
        migrations.CreateModel(
            name='StudentUploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_file', models.FileField(upload_to='documents/%Y/%m/%d')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('assignment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MainProject.Assignment')),
            ],
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]