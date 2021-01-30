from django.db import models
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Sum

import logging
logger = logging.getLogger('error_logger')

channel_layer = get_channel_layer()

# Create your models here.
class Race(models.Model):
    name = models.CharField(max_length=100, unique=True)
    polish_name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return "{}".format(self.name)

class WarriorType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    polish_name = models.CharField(max_length=100, unique=True)
    description = models.TextField() #tu pisać skąd lub na co
    race = models.ForeignKey(Race, on_delete=models.RESTRICT)
    def __str__(self):
        return "{}".format(self.name)

class Parameter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=2, unique=True)
    description = models.TextField() 
  
    def __str__(self):
        return "{}".format(self.short_name)


class WarriorLevelTemplate(models.Model):
    level = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    gold_limit = models.PositiveIntegerField()
    weapon_skill = models.PositiveIntegerField()
    ballistic_skill = models.PositiveIntegerField()
    strength = models.PositiveIntegerField()
    damage_dice = models.PositiveIntegerField()
    toughness = models.PositiveIntegerField()
    wounds_dice = models.PositiveIntegerField()
    wounds_modifier = models.PositiveIntegerField()
    initiative = models.PositiveIntegerField()
    attacks = models.PositiveIntegerField()
    luck = models.PositiveIntegerField()
    willpower = models.PositiveIntegerField()
    skills = models.PositiveIntegerField()
    pinning = models.PositiveIntegerField()
    power = models.PositiveIntegerField()
    move = models.PositiveIntegerField()
    warrior_type = models.ForeignKey(WarriorType, on_delete=models.RESTRICT)

    def __str__(self):
        return "{} level {}".format(self.warrior_type.name, self.level)
    

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField() #tu pisać skąd lub na co
    def __str__(self):
        return "{}".format(self.name)

class Character(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey('people.Person', on_delete = models.RESTRICT)
    name = models.CharField(max_length=100, unique=True)
    warrior_type = models.ForeignKey(WarriorType, on_delete=models.RESTRICT)
    battle_level = models.PositiveIntegerField(default=1)
    starting_wounds = models.PositiveIntegerField()
    leader = models.ForeignKey("self", on_delete=models.RESTRICT, related_name ='leader_set', null = True)

    def get_current_gold(self):
        return Gold.objects.filter(owner=self).aggregate(suma=Sum('amount'))['suma']

    def add_gold(self,amount, why):
        Gold.objects.create(owner = self, amount = amount, description = why) if amount>0 else None

    def remove_gold(self,amount, why):
        amount = amount if amount < self.get_current_gold() else self.get_current_gold()
        Gold.objects.create(owner = self, amount = -amount, description = why) if amount>0 else None

    def __str__(self):
        return "{}".format(self.name)

  
class Gold(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    owner = models.ForeignKey(Character, on_delete = models.CASCADE)
    description = models.TextField() #tu pisać skąd lub na co

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField() 
    def __str__(self):
        return "{}".format(self.name)

class Equipment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Character, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.RESTRICT)
    description = models.TextField() #tu pisać skąd lub na co

    def __str__(self):
        return "{}".format(self.name)

class CharacterParameter(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    character = models.ForeignKey(Character, on_delete = models.RESTRICT)
    parameter = models.ForeignKey(Parameter, on_delete = models.RESTRICT)
    value = models.IntegerField()
    description = models.CharField(max_length=256) 
 
class JourneyTable(models.Model):
    destination = models.CharField(max_length=20)
    weeks = models.PositiveIntegerField()
    rolls = models.PositiveIntegerField()
    def __str__(self):
        return ("{} - {} weeks => {} rolls".format(self.destination,self.weeks, self.rolls))

class EventType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class EventTable(models.Model):
    class Whom(models.TextChoices):
        ALL = 'ALL'
        ANY = 'ANY'
        SOME = 'SOME'
        ONE = 'ONE'
        EACH = 'EACH'

    number = models.PositiveIntegerField()
    event_type = models.ForeignKey(EventType, on_delete = models.RESTRICT)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    description_copy = models.TextField(blank=True)
    command = models.TextField(blank=True)
    whom = models.CharField(max_length=4,choices = Whom.choices, default = Whom.ONE)

    def __str__(self):
        return ("{}: {} {}".format(self.event_type.name, self.number, self.title))

class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    character = models.ForeignKey(Character, on_delete = models.CASCADE)
    event = models.ForeignKey(EventTable, on_delete = models.CASCADE)
    description = models.TextField(blank=True)
    done = models.BooleanField(default =False)
    command = models.TextField(blank=True)

def create_event_trigger(sender, instance, *args, **kwargs):
    logger.error('event of {}'.format(instance.character))
    if Event.objects.filter(character=instance.character,done=False).count() == 1:
        async_to_sync(channel_layer.group_send)("chat_{}".format(instance.character.leader.name),  {"type": "redirect", "redirect": "/show_event/"})

post_save.connect(create_event_trigger, sender=Event)

