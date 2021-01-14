# Generated by Django 3.1.5 on 2021-01-14 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_characterparameter_desc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='race',
            old_name='name',
            new_name='polish_name',
        ),
        migrations.RenameField(
            model_name='warriortype',
            old_name='name',
            new_name='polish_name',
        ),
        migrations.AddField(
            model_name='warriortype',
            name='race',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='game.race'),
            preserve_default=False,
        ),
    ]
