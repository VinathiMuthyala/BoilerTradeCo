# Generated by Django 5.0.2 on 2024-03-01 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='seller_email',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
