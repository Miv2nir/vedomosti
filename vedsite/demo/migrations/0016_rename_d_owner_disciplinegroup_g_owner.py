# Generated by Django 4.1.5 on 2023-06-04 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0015_disciplinegroup_d_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='disciplinegroup',
            old_name='d_owner',
            new_name='g_owner',
        ),
    ]