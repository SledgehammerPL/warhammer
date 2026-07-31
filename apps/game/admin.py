from django.contrib import admin
from . import models

# Register your models here.


class EventTemplateMonsterInline(admin.TabularInline):
    model = models.EventTemplateMonster
    extra = 1


class EventTemplateAdmin(admin.ModelAdmin):
    readonly_fields = ['description_copy']
    list_display = ['number', 'title', 'event_type', 'card_kind', 'draw_another_event', 'draw_treasure']
    list_filter = ['event_type', 'card_kind', 'draw_another_event', 'draw_treasure']
    search_fields = ['title', 'number']
    inlines = [EventTemplateMonsterInline]


class MonsterAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'battle_level',
        'weapon_skill',
        'ballistic_skill',
        'strength',
        'toughness',
        'wounds',
        'attacks',
        'move',
        'gold_value',
    ]
    list_filter = ['battle_level']
    search_fields = ['name']


admin.site.register(models.WarriorType)
admin.site.register(models.WarriorLevelTemplate)
admin.site.register(models.Parameter)
admin.site.register(models.Race)
admin.site.register(models.Skill)
admin.site.register(models.Shop)
admin.site.register(models.LocationTemplate)
admin.site.register(models.Character)
admin.site.register(models.Gold)
admin.site.register(models.Item)
admin.site.register(models.Equipment)
admin.site.register(models.CharacterParameter)
admin.site.register(models.JourneyTable)
admin.site.register(models.EventType)
admin.site.register(models.Monster, MonsterAdmin)
admin.site.register(models.EventTemplate, EventTemplateAdmin)
admin.site.register(models.EventTemplateMonster)
admin.site.register(models.Party)
admin.site.register(models.ObjectiveRoom)
admin.site.register(models.AdventureTemplate)
admin.site.register(models.Adventure)
admin.site.register(models.AdventureCharacter)
admin.site.register(models.Turn)
admin.site.register(models.SpellType)
admin.site.register(models.Spell)
admin.site.register(models.CharacterSpell)

