# Generated by Django 2.2.7 on 2020-09-29 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0004_auto_20200929_1505'),
        ('auth', '0011_update_proxy_permissions'),
        ('foodelivery', '0020_auto_20200929_1505'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Usser',
            new_name='User',
        ),
    ]
