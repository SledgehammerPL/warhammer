import json

from django.db import migrations

from apps.game.dungeon_event_commands import DUNGEON_EVENT_UPDATES


def apply_dungeon_event_commands(apps, schema_editor):
    EventTemplate = apps.get_model('game', 'EventTemplate')
    for template_id, payload in DUNGEON_EVENT_UPDATES.items():
        EventTemplate.objects.filter(id=template_id).update(
            before_form=payload['before_form'],
            command=json.dumps(payload['command']),
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0048_snakes_event_commands'),
    ]

    operations = [
        migrations.RunPython(apply_dungeon_event_commands, noop_reverse),
    ]
