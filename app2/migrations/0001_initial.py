# Generated by Django 5.0.2 on 2024-03-01 09:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(choices=[('Furniture', 'Furniture'), ('Appliances', 'Appliances'), ('Textbooks', 'Textbooks'), ('School supplies', 'School supplies'), ('Clothing', 'Clothing'), ('Game tickets', 'Game tickets')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='QualityTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(choices=[('Like New', 'Like New'), ('Good', 'Good'), ('Acceptable', 'Acceptable')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('seller_email', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('date_posted', models.TextField(default=0)),
                ('category_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app2.categorytag')),
                ('quality_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app2.qualitytag')),
            ],
        ),
        migrations.CreateModel(
            name='ProductListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.productinfo')),
            ],
        ),
    ]
