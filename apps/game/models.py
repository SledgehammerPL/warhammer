from django.db import models
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Sum
import re

import logging
logger = logging.getLogger('error_logger')

channel_layer = get_channel_layer()


def _chat_group_name(raw_value):
    # Channels allows only ASCII alnum, hyphen, underscore and dot.
    ascii_value = str(raw_value or "").encode("ascii", "ignore").decode("ascii")
    safe_value = re.sub(r"[^A-Za-z0-9_.-]+", "_", ascii_value).strip("_.-")
    if not safe_value:
        safe_value = "anonymous"
    return f"chat_{safe_value}"[:99]


def notify_party_redirect(leader, path='/'):
    """Ask all party browsers (WebSocket group) to navigate to path."""
    if not leader or channel_layer is None:
        return
    async_to_sync(channel_layer.group_send)(
        _chat_group_name(leader.name),
        {"type": "redirect", "redirect": path},
    )


# Item.command tokens like "Toughness+1; Movement-1" → Parameter.short_name deltas.
# "=" assignments (e.g. Strength=4 on weapons) are weapon ratings, not character mods.
_EQUIP_STAT_ALIASES = {
    'toughness': 'T',
    'strength': 'S',
    'strenght': 'S',
    'move': 'M',
    'movement': 'M',
    'weapon_skill': 'WS',
    'ballistic_skill': 'BS',
    'initiative': 'I',
    'attacks': 'A',
    'attack': 'A',
    'luck': 'L',
    'willpower': 'WP',
    'wounds': 'W',
    'pinning': 'EP',
    'escape_pining': 'EP',
}
_EQUIP_STAT_MOD_RE = re.compile(r'^([A-Za-z_]+)\s*([+-])\s*(\d+)$')


def parse_equipment_stat_modifiers(command):
    """Parse additive item.command modifiers into {Parameter.short_name: delta}."""
    mods = {}
    if not command:
        return mods
    for part in str(command).split(';'):
        part = part.strip()
        if not part:
            continue
        match = _EQUIP_STAT_MOD_RE.match(part)
        if not match:
            continue
        alias = match.group(1).lower()
        short = _EQUIP_STAT_ALIASES.get(alias)
        if not short:
            continue
        delta = int(match.group(3))
        if match.group(2) == '-':
            delta = -delta
        mods[short] = mods.get(short, 0) + delta
    return mods

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
    can_cast_spells = models.BooleanField(default=False)
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
    available_in = models.ForeignKey(Shop, on_delete=models.RESTRICT, null=True, blank=True)
    chance_to_be_in_shop = models.PositiveIntegerField(default=18)
    buy_price = models.PositiveIntegerField(default=100000)
    sell_price = models.PositiveIntegerField(default=0)
    command = models.CharField(max_length=256, blank=True)
    initial_for = models.ManyToManyField(WarriorType, blank=True, related_name='initial_items')
    is_weapon = models.BooleanField(default=False)
    is_ballistic_weapon = models.BooleanField(default=False)
    is_helmet = models.BooleanField(default=False)
    is_armour = models.BooleanField(default=False)
    is_boots = models.BooleanField(default=False)
    is_shield = models.BooleanField(default=False)
    durability = models.ForeignKey('Durability', on_delete=models.SET_NULL, null=True, blank=True)
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
    weapon = models.ForeignKey('Equipment', on_delete=models.SET_NULL, null=True, blank=True, related_name='as_weapon_for')
    ballistic_weapon = models.ForeignKey('Equipment', on_delete=models.SET_NULL, null=True, blank=True, related_name='as_ballistic_weapon_for')
    helmet = models.ForeignKey('Equipment', on_delete=models.SET_NULL, null=True, blank=True, related_name='as_helmet_for')
    armour = models.ForeignKey('Equipment', on_delete=models.SET_NULL, null=True, blank=True, related_name='as_armour_for')
    boots = models.ForeignKey('Equipment', on_delete=models.SET_NULL, null=True, blank=True, related_name='as_boots_for')
    shield = models.ForeignKey('Equipment', on_delete=models.SET_NULL, null=True, blank=True, related_name='as_shield_for')

    @property
    def is_leader(self):
        return self.leader_id == self.pk

    def get_parameter_totals(self):
        key_map = {
            'W': 'wounds',
            'M': 'move',
            'WS': 'weapon_skill',
            'BS': 'ballistic_skill',
            'S': 'strength',
            'T': 'toughness',
            'I': 'initiative',
            'A': 'attacks',
            'L': 'luck',
            'WP': 'willpower',
            'EP': 'pinning',
        }
        totals = {
            key: {'value': None}
            for key in key_map.values()
        }
        rows = (
            CharacterParameter.objects
            .filter(character=self, parameter__short_name__in=key_map.keys())
            .values('parameter__short_name')
            .annotate(value=Sum('value'))
        )
        for row in rows:
            totals[key_map[row['parameter__short_name']]] = {'value': row['value']}

        equipped_ids = [
            eid for eid in (
                self.weapon_id,
                self.ballistic_weapon_id,
                self.helmet_id,
                self.armour_id,
                self.boots_id,
                self.shield_id,
            )
            if eid
        ]
        if equipped_ids:
            for equipment in Equipment.objects.filter(id__in=equipped_ids).select_related('item'):
                for short, delta in parse_equipment_stat_modifiers(equipment.item.command).items():
                    key = key_map.get(short)
                    if not key or not delta:
                        continue
                    current = totals[key]['value']
                    totals[key]['value'] = delta if current is None else current + delta
        return totals

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
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.item.name)

class CharacterParameter(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    character = models.ForeignKey(Character, on_delete = models.RESTRICT)
    parameter = models.ForeignKey(Parameter, on_delete = models.RESTRICT)
    value = models.IntegerField()
    description = models.CharField(max_length=256) 

class Durability(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=256)
    description = models.TextField()
    def __str__(self):
        return "{}".format(self.name)

class Skill(models.Model):
    name = models.CharField(max_length=256)
    skill_type = models.ForeignKey(Durability, on_delete = models.RESTRICT)
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


class Monster(models.Model):
    """Catalog entry for a Warhammer Quest monster combat profile."""

    name = models.CharField(max_length=100, unique=True)
    weapon_skill = models.PositiveIntegerField(help_text='WS')
    ballistic_skill = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='BS target number (e.g. 5 means 5+); blank if no ranged attack',
    )
    strength = models.PositiveIntegerField(help_text='S')
    toughness = models.PositiveIntegerField(help_text='T')
    wounds = models.PositiveIntegerField(help_text='W')
    attacks = models.PositiveIntegerField(help_text='A')
    move = models.PositiveIntegerField(help_text='Move')
    gold_value = models.PositiveIntegerField(default=0)
    battle_level = models.PositiveIntegerField(
        default=1,
        help_text='Difficulty / Battle Level used when scaling encounters',
    )
    special_rules = models.TextField(
        blank=True,
        help_text='Free-text or JSON-encoded special rules from the monster card',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def as_combat_dict(self) -> dict:
        """Return a plain dict of combat stats for API / combat UI payloads."""
        return {
            'id': self.pk,
            'name': self.name,
            'WS': self.weapon_skill,
            'BS': self.ballistic_skill,
            'S': self.strength,
            'T': self.toughness,
            'W': self.wounds,
            'A': self.attacks,
            'Move': self.move,
            'gold_value': self.gold_value,
            'battle_level': self.battle_level,
            'special_rules': self.special_rules,
        }


class EventTemplate(models.Model):
    """Catalog card for dungeon / journey / settlement events.

    For the classic Unexpected Event deck (``EventType`` = 'Dungeon Events'),
    ``card_kind`` distinguishes Monster encounters (``M``) from Special events
    (``E``: traps, environment, treasures, etc.).
    """

    CARD_MONSTER = 'M'
    CARD_SPECIAL = 'E'
    CARD_KIND_CHOICES = [
        (CARD_MONSTER, 'Monster'),
        (CARD_SPECIAL, 'Special'),
    ]

    number = models.PositiveIntegerField()
    event_type = models.ForeignKey(EventType, on_delete=models.RESTRICT)
    title = models.CharField(max_length=100)
    before_form = models.TextField(blank=True)
    after_form = models.TextField(blank=True)
    description_copy = models.TextField(blank=True)
    command = models.TextField(null=False, default="{}")
    card_kind = models.CharField(
        max_length=1,
        choices=CARD_KIND_CHOICES,
        blank=True,
        null=True,
        db_index=True,
        help_text="M = Monster encounter, E = Special event (blank for non-deck events)",
    )
    draw_another_event = models.BooleanField(
        default=False,
        help_text='After resolving, draw another Unexpected Event',
    )
    draw_treasure = models.BooleanField(
        default=False,
        help_text='After resolving (typically after combat), draw a Treasure card',
    )
    monsters = models.ManyToManyField(
        Monster,
        through='EventTemplateMonster',
        related_name='event_templates',
        blank=True,
    )

    def __str__(self):
        return ("{}: {} {}".format(self.event_type.name, self.number, self.title))

    def is_monster_event(self) -> bool:
        return self.card_kind == self.CARD_MONSTER

    def is_special_event(self) -> bool:
        return self.card_kind == self.CARD_SPECIAL


class EventTemplateMonster(models.Model):
    """Links an EventTemplate to a Monster with a quantity expression.

    ``quantity`` accepts a fixed number (``"6"``) or a dice expression
    evaluated by ``eval_amount`` / ``Roll`` (e.g. ``"1D6"``, ``"1D3+1"``).
    """

    event_template = models.ForeignKey(
        EventTemplate,
        on_delete=models.CASCADE,
        related_name='monster_entries',
    )
    monster = models.ForeignKey(
        Monster,
        on_delete=models.RESTRICT,
        related_name='event_entries',
    )
    quantity = models.CharField(
        max_length=32,
        default='1',
        help_text='Fixed count or dice expression, e.g. "1D6", "1D3+1", "6"',
    )
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        unique_together = [('event_template', 'monster')]

    def __str__(self):
        return "{} × {} on {}".format(self.quantity, self.monster.name, self.event_template)

    def resolve_quantity(self) -> int:
        """Roll / evaluate ``quantity`` and return a non-negative integer count."""
        from .functions import eval_amount

        return max(0, int(eval_amount(self.quantity)))


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
        notify_party_redirect(instance.character.leader, '/show_event/')

post_save.connect(create_event_trigger, sender=Event)

class ShopStatus(models.Model):
    name = models.CharField(max_length=20)

class SettlementActivity(models.Model):
    day = models.PositiveIntegerField(default = 1)
    character =  models.ForeignKey(Character, on_delete = models.RESTRICT)
    status = models.ForeignKey(ShopStatus, on_delete = models.RESTRICT)
    location = models.ForeignKey(Location, on_delete = models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete = models.RESTRICT)


class Party(models.Model):
    leader = models.ForeignKey(Character, on_delete=models.RESTRICT, related_name='led_parties')

    def __str__(self):
        return "Party of {}".format(self.leader.name)


class ObjectiveRoom(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class AdventureTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    objective_room = models.ForeignKey(ObjectiveRoom, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.name


class Adventure(models.Model):
    template = models.ForeignKey(AdventureTemplate, on_delete=models.RESTRICT, null=True, blank=True)
    leader = models.ForeignKey(Character, on_delete=models.RESTRICT, related_name='led_adventures')
    characters = models.ManyToManyField(
        Character,
        through='AdventureCharacter',
        related_name='adventures',
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.template:
            return self.template.name
        return "Adventure {}".format(self.id)

    @classmethod
    def begin_adventure(cls, leader):
        """Pick a random AdventureTemplate, create Adventure for the party, start turn 1."""
        template = AdventureTemplate.objects.order_by('?').first()
        if template is None:
            raise AdventureTemplate.DoesNotExist('No AdventureTemplate available')

        adventure = cls.objects.create(template=template, leader=leader)

        companions = Character.objects.filter(leader=leader).order_by('id')
        AdventureCharacter.objects.bulk_create([
            AdventureCharacter(adventure=adventure, character=companion, order=order)
            for order, companion in enumerate(companions)
        ])

        adventure.begin_turn()
        return adventure

    def get_power_reroll_character(self):
        """Wizard in the party decides power re-roll; otherwise the leader."""
        wizard = (
            self.characters
            .filter(warrior_type__can_cast_spells=True)
            .order_by('adventurecharacter__order', 'id')
            .first()
        )
        return wizard or self.leader

    def begin_turn(self):
        """Create next Turn with rolled power_level; next_character is the party leader."""
        from random import randint

        last = self.turns.order_by('-turn_number').first()
        turn_number = (last.turn_number + 1) if last else 1
        power_level = randint(1, 6)
        turn = Turn.objects.create(
            adventure=self,
            turn_number=turn_number,
            power_level=power_level,
            next_character=self.leader,
        )
        if power_level == 1:
            turn.power_reroll_pending = True
            turn.power_reroll_for = self.get_power_reroll_character()
            turn.save(update_fields=['power_reroll_pending', 'power_reroll_for'])
        return turn

    def end_turn(self):
        """Finish the current turn. Placeholder for future cleanup."""
        return self.turns.order_by('-turn_number').first()

    def next_turn(self):
        """End current turn and start the next one."""
        self.end_turn()
        return self.begin_turn()


class AdventureCharacter(models.Model):
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = [('adventure', 'character')]


class Turn(models.Model):
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE, related_name='turns')
    turn_number = models.PositiveIntegerField(default=1)
    power_level = models.PositiveIntegerField(default=0)
    next_character = models.ForeignKey(
        Character,
        on_delete=models.RESTRICT,
        null=True, blank=True,
        related_name='next_turns',
    )
    power_reroll_pending = models.BooleanField(default=False)
    power_reroll_for = models.ForeignKey(
        Character,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='power_reroll_turns',
    )

    class Meta:
        ordering = ['turn_number']

    def __str__(self):
        return "Turn {} (Adventure: {})".format(self.turn_number, self.adventure)

    def resolve_power_reroll(self, accept_reroll):
        """Yes → re-roll power once; No → keep 1.
        Unexpected dungeon event on No, or if the re-roll is also 1.
        Returns True when an unexpected event was triggered.
        """
        from random import randint

        if not self.power_reroll_pending:
            return False

        unexpected = False
        if accept_reroll:
            self.power_level = randint(1, 6)
            unexpected = self.power_level == 1
        else:
            unexpected = True

        self.power_reroll_pending = False
        self.power_reroll_for = None
        self.save(update_fields=['power_level', 'power_reroll_pending', 'power_reroll_for'])

        if unexpected:
            from apps.game.functions import roll_unexpected_dungeon_event
            roll_unexpected_dungeon_event(self.adventure.leader)
        return unexpected


class SpellType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Spell(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    cost = models.PositiveIntegerField(default=0)
    spell_type = models.ForeignKey(SpellType, on_delete=models.RESTRICT, null=True, blank=True)
    characters = models.ManyToManyField(
        'Character',
        through='CharacterSpell',
        related_name='known_spells',
        blank=True,
    )

    def __str__(self):
        return self.name


class CharacterSpell(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='spells')
    spell = models.ForeignKey(Spell, on_delete=models.RESTRICT)
    description = models.TextField(blank=True)

    def __str__(self):
        return "{} – {}".format(self.character.name, self.spell.name)

