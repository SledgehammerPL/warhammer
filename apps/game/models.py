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
    alehouse_roll = models.CharField(max_length=10, default='2D6')
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

class ShopType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    availability = models.PositiveIntegerField(default=1)
    def __str__(self):
        return "{}".format(self.name)

class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    shop_type = models.ForeignKey(ShopType, on_delete=models.RESTRICT, null=True)
    forbidden = models.ManyToManyField(WarriorType)

    def __str__(self):
        return "{}".format(self.name)

class Item(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    restriction = models.ManyToManyField(WarriorType)
    available_in = models.ForeignKey(Shop, on_delete=models.RESTRICT,null=True)
    chance_to_be_in_shop = models.PositiveIntegerField(default=18)
    buy_price = models.PositiveIntegerField(default=100000)
    sell_price = models.PositiveIntegerField(default=0)
    command = models.CharField(max_length=256, blank=True)
    def __str__(self):
        return "{} ({})".format(self.name, self.code)
  
class LocationTemplate(models.Model):
    name = models.CharField(max_length=100)
    character_position = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=20, unique = True)
    weeks_of_journey_to = models.PositiveIntegerField(default=0)
    is_settlement = models.BooleanField(default=False)
    is_journey = models.BooleanField(default=False)
    next_location = models.ManyToManyField('self')
    next_location_desc = models.CharField(max_length=100)
    next_location_url = models.CharField(max_length=100)
    no_of_dices = models.PositiveIntegerField(default=0)
    living_expenses = models.PositiveIntegerField(default=1)
    name_of_period = models.CharField(max_length=4, default='day')
    def __str__(self):
        return "{}".format(self.name)
class Location(models.Model):
    name = models.CharField(max_length=100)
    template = models.ForeignKey(LocationTemplate, on_delete = models.RESTRICT, null=True, blank=True)
    next_location = models.ForeignKey('self', on_delete = models.RESTRICT, null=True, blank=True)

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
    location = models.ForeignKey(Location, on_delete=models.RESTRICT, default=0)
    active_day = models.BooleanField(default=False)
    ticks = models.PositiveIntegerField(default=1)

    def get_current_gold(self):
        return Gold.objects.filter(owner=self).aggregate(suma=Sum('amount'))['suma']

    def add_gold(self,amount, why):
        Gold.objects.create(owner = self, amount = amount, description = why) if amount>0 else None
        return self.get_current_gold()

    def remove_gold(self,amount, why):
        amount = amount if amount < self.get_current_gold() else self.get_current_gold()
        Gold.objects.create(owner = self, amount = -amount, description = why) if amount>0 else None
        return self.get_current_gold()

    def remove_gold_and_most_valuable_item_if_not_enough(self, amount, why):
        mvi_name = False
        if self.get_current_gold()<amount:
            try:
                most_valuable_item = self.equipment_set.order_by('-item__sell_price')[0]
                mvi_name = most_valuable_item.item.name
                most_valuable_item.delete()
            except IndexError:
                pass

        self.remove_gold(amount,why)
        return (self.get_current_gold(),mvi_name)

    def pay_living_expenses(self):
        living_expenses = self.location.template.living_expenses
        if self.get_current_gold()>living_expenses:
            self.remove_gold(living_expenses, 'Living Expenses in {}'.format(self.location.name))
            return True
        else:
            return False

    def buy_item(self, code, price, seller):
        if self.get_current_gold()>=price:
            item= Item.objects.get(code=code)
            Gold.objects.create(amount=-price, description="{} bought from {}".format(item, seller), owner=self)
            Equipment.objects.create(item=item, owner=self, description="bought from {}".format(seller))
            return True
        else:
            return False
    def sell_item(self, code, price, buyer):
        item= Item.objects.get(code=code)
        to_sell=Equipment.objects.filter(item=item, owner=self)
        if to_sell.count()>0: 
            Gold.objects.create(amount=+price, description="{} sold to {}".format(item, buyer), owner=self)
            to_sell[0].delete()
            if to_sell.count()>0:
                return True
            return False
        return False


    def __str__(self):
        return "{}".format(self.name)

  
class Gold(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    owner = models.ForeignKey(Character, on_delete = models.CASCADE)
    description = models.TextField() #tu pisać skąd lub na co

class Equipment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Character, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.RESTRICT)
    description = models.TextField() #tu pisać skąd lub na co

    def __str__(self):
        return "{}".format(self.item.name)

class CharacterParameter(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    character = models.ForeignKey(Character, on_delete = models.RESTRICT)
    parameter = models.ForeignKey(Parameter, on_delete = models.RESTRICT)
    value = models.IntegerField()
    description = models.CharField(max_length=256) 

class SkillType(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=256)
    description = models.TextField()
    def __str__(self):
        return "{}".format(self.name)

class Skill(models.Model):
    name = models.CharField(max_length=256)
    skill_type = models.ForeignKey(SkillType, on_delete = models.RESTRICT)
    description = models.TextField() #tu pisać skąd lub na co
    restriction = models.ManyToManyField(WarriorType)

    def __str__(self):
        return "{}".format(self.name)

class CharacterSkill(models.Model):
    character = models.ForeignKey(Character, on_delete = models.RESTRICT)
    skill = models.ForeignKey(Skill, on_delete = models.RESTRICT)
    description = models.TextField() #tu pisać skąd lub na co


class JourneyTable(models.Model):
    location = models.ForeignKey(LocationTemplate, on_delete = models.RESTRICT, null=True)
    destination = models.CharField(max_length=20)
    weeks = models.PositiveIntegerField()
    rolls = models.PositiveIntegerField()
    def __str__(self):
        return ("{} - {} weeks => {} rolls".format(self.destination,self.weeks, self.rolls))

class EventType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class EventTemplate(models.Model):
    number = models.PositiveIntegerField()
    event_type = models.ForeignKey(EventType, on_delete = models.RESTRICT)
    title = models.CharField(max_length=100)
    before_form = models.TextField(blank=True)
    after_form = models.TextField(blank=True)
    description_copy = models.TextField(blank=True)
    command = models.TextField(null=False, default="{}")

    def __str__(self):
        return ("{}: {} {}".format(self.event_type.name, self.number, self.title))

class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    character = models.ForeignKey(Character, on_delete = models.CASCADE)
    template = models.ForeignKey(EventTemplate, on_delete = models.CASCADE)
    before_form = models.TextField(blank=True)
    after_form = models.TextField(blank=True)
    done = models.BooleanField(default =False)
    command = models.TextField(blank=True)
    leader_event = models.ForeignKey("self", on_delete = models.CASCADE, null = True)

def create_event_trigger(sender, instance, *args, **kwargs):
    logger.error('event of {}'.format(instance.character))
    if Event.objects.filter(character=instance.character,done=False).count() == 1:
        async_to_sync(channel_layer.group_send)("chat_{}".format(instance.character.leader.name),  {"type": "redirect", "redirect": "/show_event/"})

post_save.connect(create_event_trigger, sender=Event)

class ShopStatus(models.Model):
    name = models.CharField(max_length=20)

class SettlementActivity(models.Model):
    day = models.PositiveIntegerField(default = 1)
    character =  models.ForeignKey(Character, on_delete = models.RESTRICT)
    status = models.ForeignKey(ShopStatus, on_delete = models.RESTRICT)
    location = models.ForeignKey(Location, on_delete = models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete = models.RESTRICT)

