# Generated by Django 4.1.5 on 2023-05-25 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0010_groups_students_delete_student_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discipline',
            name='d_children',
        ),
    ]