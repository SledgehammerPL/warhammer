import json

import django.db.models.deletion
from django.db import migrations, models

SNAKES_BEFORE_FORM = """Without warning, hundreds of snakes suddenly drop into the room through carefully concealed holes in the roof. Each Warrior is quickly covered in a writhing mass of venomous serpents.

{{ each_warrior_print }}

{{ party_print }}"""

SNAKES_COMMAND = {
    "0": {
        "party_print": "Draw another Event card immediately.",
        "party_command": "dungeon_event+1",
    },
    "1": {
        "each_warrior_print": (
            "The snakes manage to bite your Warrior, finding chinks in even the toughest armour. "
            "He suffers 1D6 Wounds, with no modifiers for Toughness or armour. "
            "He cannot do anything for the rest of the turn, and any Monster who attacks him gets +1 on its to hit rolls. "
            "At the start of the next Warriors' Phase, roll on this table again."
        ),
        "each_warrior_command": "Wounds-1D6",
    },
    "2": {
        "each_warrior_print": (
            "The snakes manage to bite your Warrior, finding chinks in even the toughest armour. "
            "He suffers 1D6 Wounds, with no modifiers for Toughness or armour. "
            "He cannot do anything for the rest of the turn, and any Monster who attacks him gets +1 on its to hit rolls. "
            "At the start of the next Warriors' Phase, roll on this table again."
        ),
        "each_warrior_command": "Wounds-1D6",
    },
    "3": {
        "each_warrior_print": (
            "The snakes manage to bite your Warrior. He suffers 1D6 Wounds, with no modifiers for Toughness or armour. "
            "He then manages to free himself from the writhing mass and slashes the foul creatures to pieces."
        ),
        "each_warrior_command": "Wounds-1D6",
    },
    "4": {
        "each_warrior_print": (
            "The snakes manage to bite your Warrior. He suffers 1D6 Wounds, with no modifiers for Toughness or armour. "
            "He then manages to free himself from the writhing mass and slashes the foul creatures to pieces."
        ),
        "each_warrior_command": "Wounds-1D6",
    },
    "5": {
        "each_warrior_print": (
            "Your Warrior nimbly avoids the snakes as they drop from above, killing them as they fall at his feet. "
            "The attack has no effect."
        ),
    },
    "6": {
        "each_warrior_print": (
            "Your Warrior nimbly avoids the snakes as they drop from above, killing them as they fall at his feet. "
            "The attack has no effect."
        ),
    },
}


def apply_snakes_commands(apps, schema_editor):
    EventTemplate = apps.get_model('game', 'EventTemplate')
    EventTemplate.objects.filter(id=83).update(
        before_form=SNAKES_BEFORE_FORM,
        command=json.dumps(SNAKES_COMMAND),
    )


def revert_snakes_commands(apps, schema_editor):
    EventTemplate = apps.get_model('game', 'EventTemplate')
    EventTemplate.objects.filter(id=83).update(command='{}')


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0046_set_helmet_item_flags'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='power_reroll_for',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='power_reroll_turns',
                to='game.character',
            ),
        ),
        migrations.AddField(
            model_name='turn',
            name='power_reroll_pending',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(apply_snakes_commands, revert_snakes_commands),
    ]
