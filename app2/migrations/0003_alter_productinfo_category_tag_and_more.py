# Generated by Django 5.0.2 on 2024-03-29 08:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0002_alter_categorytag_options_remove_productinfo_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='category_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app2.categorytag'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='quality_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app2.qualitytag'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='seller_email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL),
        ),
    ]