# Generated by Django 2.2.7 on 2020-09-10 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodelivery', '0002_auto_20200909_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='resturants',
            name='slug',
            field=models.SlugField(default='test'),
            preserve_default=False,
        ),
    ]
