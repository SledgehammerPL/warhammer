# Generated by Django 3.1.5 on 2021-01-16 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_warriorleveltemplate_move'),
    ]

    operations = [
        migrations.AddField(
            model_name='warriorleveltemplate',
            name='power',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
