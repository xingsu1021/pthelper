# Generated by Django 4.1 on 2022-10-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0018_alter_config_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='rate',
            field=models.CharField(default='all', max_length=10, verbose_name='码率:all,1080,2160'),
        ),
    ]