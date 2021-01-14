from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(WarriorType)
admin.site.register(WarriorLevelTemplate)
admin.site.register(Parameter)
admin.site.register(Race)
admin.site.register(Skill)
admin.site.register(Character)
admin.site.register(Gold)
admin.site.register(Item)
admin.site.register(Equipment)
admin.site.register(CharacterParameter)

