# Generated by Django 4.1.5 on 2023-05-22 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0008_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_id', models.UUIDField()),
                ('d_name', models.CharField(max_length=200)),
                ('d_owner', models.CharField(max_length=200)),
                ('d_children', models.CharField(max_length=200)),
            ],
        ),
    ]
