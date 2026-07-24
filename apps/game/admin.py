from django.contrib import admin
from . import models

# Register your models here.


class EventTemplateAdmin(admin.ModelAdmin):
    readonly_fields = ['description_copy']


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
admin.site.register(models.EventTemplate,EventTemplateAdmin)
admin.site.register(models.Party)
admin.site.register(models.ObjectiveRoom)
admin.site.register(models.AdventureTemplate)
admin.site.register(models.Adventure)
admin.site.register(models.AdventureCharacter)
admin.site.register(models.Turn)
admin.site.register(models.SpellType)
admin.site.register(models.Spell)
admin.site.register(models.CharacterSpell)

