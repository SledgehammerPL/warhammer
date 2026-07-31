import json

from django.db import migrations

from apps.game.dungeon_event_commands import DUNGEON_EVENT_UPDATES


def update_spiked_pit_template(apps, schema_editor):
    EventTemplate = apps.get_model('game', 'EventTemplate')
    payload = DUNGEON_EVENT_UPDATES[85]
    EventTemplate.objects.filter(id=85).update(
        before_form=payload['before_form'],
        command=json.dumps(payload['command']),
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0049_dungeon_event_commands'),
    ]

    operations = [
        migrations.RunPython(update_spiked_pit_template, noop_reverse),
    ]
