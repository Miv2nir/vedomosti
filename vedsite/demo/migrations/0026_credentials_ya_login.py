# Generated by Django 4.1.5 on 2023-06-11 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0025_remove_credentials_ya_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='credentials',
            name='ya_login',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
