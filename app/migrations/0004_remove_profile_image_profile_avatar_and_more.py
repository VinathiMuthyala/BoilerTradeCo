# Generated by Django 5.0.2 on 2024-02-29 05:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
