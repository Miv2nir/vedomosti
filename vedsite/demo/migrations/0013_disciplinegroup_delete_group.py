# Generated by Django 4.1.5 on 2023-05-25 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0012_rename_groups_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisciplineGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_id', models.UUIDField()),
                ('g_number', models.IntegerField()),
                ('g_table', models.FilePathField(blank=True)),
                ('d_id', models.UUIDField()),
            ],
            options={
                'verbose_name': 'Student Group',
                'verbose_name_plural': 'Student Groups',
            },
        ),
        migrations.DeleteModel(
            name='Group',
        ),
    ]
