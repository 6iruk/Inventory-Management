# Generated by Django 5.1.5 on 2025-03-28 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_material_purchase_date_material_purchase_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='code',
            field=models.CharField(default='Abebe-1', max_length=100),
            preserve_default=False,
        ),
    ]
