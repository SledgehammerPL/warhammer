# Generated by Django 3.1.5 on 2021-01-14 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_auto_20210114_1346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='race',
            old_name='original_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='warriortype',
            old_name='original_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='character',
            name='race',
        ),
    ]
