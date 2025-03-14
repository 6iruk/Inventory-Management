# Generated by Django 5.1.5 on 2025-03-14 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_rename_unit_price_material_selling_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
