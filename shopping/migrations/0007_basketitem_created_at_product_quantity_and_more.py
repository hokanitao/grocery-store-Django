# Generated by Django 4.2.20 on 2025-05-06 19:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0006_rename_userid_basket_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='basket',
            name='basket_status',
            field=models.CharField(choices=[('pen', 'Pending'), ('con', 'Confirmed'), ('can', 'Canceled')], default='pen', help_text='Shopping Basket Status', max_length=3),
        ),
    ]
