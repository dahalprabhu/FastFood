# Generated by Django 2.2.7 on 2020-09-23 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodelivery', '0012_auto_20200922_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditems',
            name='price',
            field=models.IntegerField(),
        ),
    ]
