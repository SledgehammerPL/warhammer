# Generated by Django 3.1.5 on 2021-01-13 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_warriortypeparametersleveltemplate_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarriorTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=100)),
                ('gold_limit', models.PositiveIntegerField()),
                ('weapon_skill', models.PositiveIntegerField()),
                ('ballistic_skill', models.PositiveIntegerField()),
                ('strength', models.PositiveIntegerField()),
                ('damage_dice', models.PositiveIntegerField()),
                ('toughness', models.PositiveIntegerField()),
                ('wounds', models.PositiveIntegerField()),
                ('initiative', models.PositiveIntegerField()),
                ('attacks', models.PositiveIntegerField()),
                ('luck', models.PositiveIntegerField()),
                ('willpower', models.PositiveIntegerField()),
                ('skills', models.PositiveIntegerField()),
                ('pinning', models.PositiveIntegerField()),
                ('warrior_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='game.warriortype')),
            ],
        ),
        migrations.RenameModel(
            old_name='LevelTemplate',
            new_name='oldLevelTemplate',
        ),
        migrations.DeleteModel(
            name='WarriorTypeParametersLevelTemplate',
        ),
    ]
