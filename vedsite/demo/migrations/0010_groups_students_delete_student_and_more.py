# Generated by Django 4.1.5 on 2023-05-25 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0009_discipline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_id', models.UUIDField()),
                ('g_number', models.IntegerField()),
                ('g_table', models.FilePathField()),
                ('d_id', models.UUIDField()),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_id', models.UUIDField()),
                ('s_name', models.CharField(max_length=200)),
                ('s_email', models.CharField(max_length=2000)),
                ('g_id', models.UUIDField()),
                ('g_number', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.AlterModelOptions(
            name='discipline',
            options={'verbose_name': 'Discipline', 'verbose_name_plural': 'Disciplines'},
        ),
    ]
