# Generated by Django 2.2.7 on 2020-09-10 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodelivery', '0005_auto_20200910_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order_quantity',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
