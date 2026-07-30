from django.db import migrations

HELMET_CODES = ('Leather_Helm', 'Open_Helmet', 'Warhelm')


def set_helmet_flags(apps, schema_editor):
    Item = apps.get_model('game', 'Item')
    Item.objects.filter(code__in=HELMET_CODES).update(is_helmet=True)


def unset_helmet_flags(apps, schema_editor):
    Item = apps.get_model('game', 'Item')
    Item.objects.filter(code__in=HELMET_CODES).update(is_helmet=False)


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0045_set_boots_item_flag'),
    ]

    operations = [
        migrations.RunPython(set_helmet_flags, unset_helmet_flags),
    ]
