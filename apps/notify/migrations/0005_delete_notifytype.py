# Generated by Django 4.0.2 on 2022-02-28 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0004_mailtype_remove_notifyconfig_smtp_is_tls_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NotifyType',
        ),
    ]
