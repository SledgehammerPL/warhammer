# Generated by Django 3.1.5 on 2021-01-25 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0031_auto_20210117_2258'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.character')),
            ],
        ),
        migrations.RenameModel(
            old_name='Event',
            new_name='EventTable',
        ),
        migrations.RenameModel(
            old_name='Journey',
            new_name='JourneyTable',
        ),
        migrations.DeleteModel(
            name='Party',
        ),
    ]