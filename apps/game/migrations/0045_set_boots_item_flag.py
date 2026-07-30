from django.db import migrations


def set_equipment_slot_flags(apps, schema_editor):
    Item = apps.get_model('game', 'Item')
    Item.objects.filter(code='Boots').update(is_boots=True)


def unset_equipment_slot_flags(apps, schema_editor):
    Item = apps.get_model('game', 'Item')
    Item.objects.filter(code='Boots').update(is_boots=False)


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0044_character_armour_character_ballistic_weapon_and_more'),
    ]

    operations = [
        migrations.RunPython(set_equipment_slot_flags, unset_equipment_slot_flags),
    ]
