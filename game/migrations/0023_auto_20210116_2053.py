# Generated by Django 3.1.5 on 2021-01-16 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0022_auto_20210116_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='party',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='game.party'),
        ),
    ]
