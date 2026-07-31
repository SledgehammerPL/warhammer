from django.db import migrations

from apps.game.monster_catalog import CORE_MONSTER_NAMES, CORE_MONSTERS


def seed_core_monsters(apps, schema_editor):
    Monster = apps.get_model('game', 'Monster')
    for payload in CORE_MONSTERS:
        Monster.objects.update_or_create(
            name=payload['name'],
            defaults={
                'weapon_skill': payload['weapon_skill'],
                'ballistic_skill': payload['ballistic_skill'],
                'strength': payload['strength'],
                'toughness': payload['toughness'],
                'wounds': payload['wounds'],
                'attacks': payload['attacks'],
                'move': payload['move'],
                'gold_value': payload['gold_value'],
                'battle_level': payload['battle_level'],
                'special_rules': payload['special_rules'],
            },
        )


def unseed_core_monsters(apps, schema_editor):
    Monster = apps.get_model('game', 'Monster')
    Monster.objects.filter(name__in=CORE_MONSTER_NAMES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0051_monster_and_event_card_kind'),
    ]

    operations = [
        migrations.RunPython(seed_core_monsters, unseed_core_monsters),
    ]
