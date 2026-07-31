from django.db import migrations

from apps.game.monster_catalog import TABLE_MONSTER_NAMES, TABLE_MONSTERS


def seed_table_monsters(apps, schema_editor):
    Monster = apps.get_model('game', 'Monster')
    for payload in TABLE_MONSTERS:
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


def unseed_table_monsters(apps, schema_editor):
    Monster = apps.get_model('game', 'Monster')
    Monster.objects.filter(name__in=TABLE_MONSTER_NAMES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0052_seed_core_monsters'),
    ]

    operations = [
        migrations.RunPython(seed_table_monsters, unseed_table_monsters),
    ]
