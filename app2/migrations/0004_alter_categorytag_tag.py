# Generated by Django 5.0.2 on 2024-04-13 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0003_bookmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorytag',
            name='tag',
            field=models.CharField(choices=[('Furniture', 'Furniture'), ('Appliances', 'Appliances'), ('Textbooks', 'Textbooks'), ('School Supplies', 'School Supplies'), ('Clothing', 'Clothing'), ('Game Tickets', 'Game Tickets'), ('Other', 'Other')], max_length=100),
        ),
    ]
