# Generated by Django 4.1.5 on 2023-06-11 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0028_credentials_ya_login'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='credentials',
            options={'verbose_name': 'Credentials', 'verbose_name_plural': 'Credentials'},
        ),
        migrations.AddField(
            model_name='credentials',
            name='stepik_id',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
