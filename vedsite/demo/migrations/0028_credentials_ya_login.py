# Generated by Django 4.1.5 on 2023-06-11 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0027_remove_credentials_ya_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='credentials',
            name='ya_login',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
