# Generated by Django 5.0.2 on 2024-04-06 06:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(choices=[('Furniture', 'Furniture'), ('Appliances', 'Appliances'), ('Textbooks', 'Textbooks'), ('School supplies', 'School supplies'), ('Clothing', 'Clothing'), ('Game tickets', 'Game tickets'), ('Other', 'Other')], max_length=100)),
            ],
            options={
                'verbose_name_plural': 'CategoryTag',
                'ordering': ('tag',),
            },
        ),
        migrations.CreateModel(
            name='QualityTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(choices=[('Like New', 'Like New'), ('Good', 'Good'), ('Acceptable', 'Acceptable')], max_length=100)),
            ],
            options={
                'verbose_name_plural': 'QualityTag',
            },
        ),
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('date_posted', models.DateTimeField(default=0)),
                ('category_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.categorytag')),
                ('seller_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('quality_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.qualitytag')),
            ],
            options={
                'verbose_name_plural': 'ProductInfo',
            },
        ),
        migrations.CreateModel(
            name='ProductListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.productinfo')),
            ],
            options={
                'verbose_name_plural': 'ProductListing',
            },
        ),
    ]
