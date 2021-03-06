# Generated by Django 4.0.2 on 2022-02-23 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='名称,特定:iyuu,telegram,email')),
                ('iyuu_key', models.CharField(max_length=200, verbose_name='IYUU令牌')),
                ('tg_chat_id', models.BigIntegerField(verbose_name='频道ID或自身id')),
                ('tg_token', models.CharField(max_length=200, verbose_name='telegram令牌')),
                ('smtp_server', models.CharField(max_length=100, verbose_name='发信地址')),
                ('smtp_port', models.IntegerField(verbose_name='发信端口')),
                ('smtp_user', models.CharField(max_length=100, verbose_name='发信账号')),
                ('smtp_password', models.CharField(max_length=128, verbose_name='发信账号密码')),
                ('smtp_is_tls', models.BooleanField(default=False, verbose_name='是否启用tls')),
                ('receive_user', models.CharField(max_length=100, verbose_name='接收账号,默认为发信账号')),
            ],
        ),
        migrations.CreateModel(
            name='NotifyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='名称')),
                ('type_id', models.IntegerField(unique=True, verbose_name='类型ID')),
            ],
        ),
    ]
