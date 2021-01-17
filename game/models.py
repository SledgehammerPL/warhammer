from django.db import models

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

class Party(models.Model):
    leader = models.ForeignKey('Character', on_delete=models.RESTRICT, related_name='+')
    
    class Meta:
        verbose_name = "party"
        verbose_name_plural = "parties"

    def __str__(self):
        return "{}'s party".format(self.leader)

class Character(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey('people.Person', on_delete = models.RESTRICT)
    name = models.CharField(max_length=100, unique=True)
    warrior_type = models.ForeignKey(WarriorType, on_delete=models.RESTRICT)
    battle_level = models.PositiveIntegerField(default=1)
    starting_wounds = models.PositiveIntegerField()
    leader = models.ForeignKey("self", on_delete=models.RESTRICT, related_name ='leader_set')
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
 
class Journey(models.Model):
    destination = models.CharField(max_length=20)
    weeks = models.PositiveIntegerField()
    rolls = models.PositiveIntegerField()
    def __str__(self):
        return ("{} - {} weeks => {} rolls".format(self.destination,self.weeks, self.rolls))

class EventType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Event(models.Model):
    number = models.PositiveIntegerField()
    event_type = models.ForeignKey(EventType, on_delete = models.RESTRICT)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return ("{}: {} {}".format(self.event_type.name, self.number, self.title))

