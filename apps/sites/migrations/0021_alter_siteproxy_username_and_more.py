# Generated by Django 4.1 on 2023-01-31 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0020_siteinfo_siteproxy_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteproxy',
            name='username',
            field=models.CharField(max_length=50, null=True, verbose_name='账号'),
        ),
        migrations.AlterField(
            model_name='siteproxy',
            name='userpassword',
            field=models.CharField(max_length=128, null=True, verbose_name='密码'),
        ),
    ]