# Generated by Django 4.0.2 on 2022-03-06 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaiDuOcr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(max_length=50, unique=True, verbose_name='APP_ID')),
                ('app_key', models.CharField(max_length=50, unique=True, verbose_name='API_KEY')),
                ('secret_key', models.CharField(max_length=50, unique=True, verbose_name='SECRET_KEY')),
            ],
        ),
    ]
