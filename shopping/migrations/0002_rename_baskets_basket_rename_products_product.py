# Generated by Django 4.2.20 on 2025-05-06 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Baskets',
            new_name='Basket',
        ),
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]
