# Generated by Django 4.0.2 on 2022-02-22 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siterank',
            name='up_time',
            field=models.IntegerField(verbose_name='升级时间,单位周'),
        ),
    ]
