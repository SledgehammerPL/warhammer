from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0035_party_adventuretemplate_adventure_adventurecharacter_turn_spell_characterspell'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='initial_for',
            field=models.ManyToManyField(blank=True, related_name='initial_items', to='game.warriortype'),
        ),
    ]
