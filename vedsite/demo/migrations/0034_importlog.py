# Generated by Django 4.1.5 on 2023-06-12 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0033_remove_student_s_display_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i_id', models.UUIDField()),
                ('g_number', models.IntegerField()),
                ('i_type', models.CharField(max_length=100)),
                ('i_contest', models.IntegerField()),
                ('t_col', models.IntegerField(default=2)),
            ],
        ),
    ]
