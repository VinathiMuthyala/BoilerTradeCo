# Generated by Django 5.0.2 on 2024-04-19 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0006_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='previous_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
