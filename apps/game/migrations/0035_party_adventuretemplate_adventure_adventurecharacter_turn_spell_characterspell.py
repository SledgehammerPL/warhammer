import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0034_shopstatus_shoptype_skilltype_remove_event_event_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='led_parties', to='game.character')),
            ],
        ),
        migrations.CreateModel(
            name='AdventureTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Adventure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='led_adventures', to='game.character')),
            ],
        ),
        migrations.CreateModel(
            name='AdventureCharacter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('adventure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.adventure')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.character')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('adventure', 'character')},
            },
        ),
        migrations.AddField(
            model_name='adventure',
            name='characters',
            field=models.ManyToManyField(related_name='adventures', through='game.AdventureCharacter', to='game.character'),
        ),
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn_number', models.PositiveIntegerField(default=1)),
                ('power_level', models.PositiveIntegerField(default=0)),
                ('adventure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turns', to='game.adventure')),
                ('next_character', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='next_turns', to='game.character')),
            ],
            options={
                'ordering': ['turn_number'],
            },
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('cost', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterSpell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spells', to='game.character')),
                ('spell', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='game.spell')),
            ],
        ),
    ]
