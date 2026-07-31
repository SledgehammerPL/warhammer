"""Warhammer Quest (1995) monster combat profiles.

Profiles follow the Roleplay Book bestiary used by the Monster Tables
(Event cards / D66 tables). Toughness is the base characteristic; armour
bonuses are noted in special_rules (e.g. T 4(6) with Armour 2).
"""

# ballistic_skill: target number for N+ (e.g. 4 => 4+); None = no ranged attack.

CORE_MONSTERS = [
    {'name': 'Giant Bat', 'weapon_skill': 2, 'ballistic_skill': None, 'strength': 2, 'toughness': 2, 'wounds': 1, 'attacks': 1, 'move': 8, 'gold_value': 15, 'battle_level': 1, 'special_rules': 'Ambush A; Fly. Damage 1D6.'},
    {'name': 'Giant Spider', 'weapon_skill': 2, 'ballistic_skill': None, 'strength': 1, 'toughness': 2, 'wounds': 1, 'attacks': 1, 'move': 6, 'gold_value': 15, 'battle_level': 1, 'special_rules': 'Web (1D3). Damage via Web bite (special).'},
    {'name': 'Giant Rat', 'weapon_skill': 2, 'ballistic_skill': None, 'strength': 3, 'toughness': 3, 'wounds': 1, 'attacks': 1, 'move': 6, 'gold_value': 25, 'battle_level': 1, 'special_rules': 'Deathleap: on hit deal 2D6+2 damage; after attacking roll 1D6 — on 3-6 the Rat is automatically killed.'},
    {'name': 'Snotling', 'weapon_skill': 1, 'ballistic_skill': None, 'strength': 1, 'toughness': 1, 'wounds': 1, 'attacks': 1, 'move': 4, 'gold_value': 10, 'battle_level': 1, 'special_rules': 'Ambush, Magic A; Gang Up. Damage Special (Gang Up).'},
    {'name': 'Goblin Spearman', 'weapon_skill': 2, 'ballistic_skill': None, 'strength': 3, 'toughness': 3, 'wounds': 2, 'attacks': 1, 'move': 4, 'gold_value': 20, 'battle_level': 1, 'special_rules': 'Armed with Spears (Fight in Ranks). Damage 1D6.'},
    {'name': 'Night Goblin Archer', 'weapon_skill': 2, 'ballistic_skill': 5, 'strength': 3, 'toughness': 3, 'wounds': 2, 'attacks': 1, 'move': 4, 'gold_value': 20, 'battle_level': 1, 'special_rules': 'Armed with Bow (Str 1). Damage 1D6.'},
    {'name': 'Orc Warrior', 'weapon_skill': 3, 'ballistic_skill': None, 'strength': 3, 'toughness': 4, 'wounds': 3, 'attacks': 1, 'move': 4, 'gold_value': 55, 'battle_level': 1, 'special_rules': 'Armed with Swords. Damage 1D6.'},
    {'name': 'Orc Archer', 'weapon_skill': 3, 'ballistic_skill': 4, 'strength': 3, 'toughness': 4, 'wounds': 3, 'attacks': 1, 'move': 4, 'gold_value': 55, 'battle_level': 1, 'special_rules': 'Armed with Bow (Str 3). Damage 1D6.'},
    {'name': 'Skaven Warrior', 'weapon_skill': 3, 'ballistic_skill': 4, 'strength': 3, 'toughness': 3, 'wounds': 3, 'attacks': 1, 'move': 5, 'gold_value': 40, 'battle_level': 1, 'special_rules': 'Skaven Clanrat. Damage 1D6.'},
    {'name': 'Minotaur', 'weapon_skill': 4, 'ballistic_skill': 4, 'strength': 4, 'toughness': 4, 'wounds': 15, 'attacks': 2, 'move': 6, 'gold_value': 440, 'battle_level': 1, 'special_rules': 'Fear 5. Damage 2D6.'},
]

TABLE_MONSTERS = [
    # Roleplay Book Monster Table entries beyond the boxed-set Event cards.
    {'name': 'Ogre', 'weapon_skill': 3, 'ballistic_skill': 5, 'strength': 4, 'toughness': 5, 'wounds': 13, 'attacks': 2, 'move': 6, 'gold_value': 400, 'battle_level': 1, 'special_rules': 'Fear 5. Damage 1D6/2D6 (5+).'},
    {'name': 'Centaur', 'weapon_skill': 3, 'ballistic_skill': 3, 'strength': 4, 'toughness': 3, 'wounds': 12, 'attacks': 2, 'move': 8, 'gold_value': 300, 'battle_level': 1, 'special_rules': 'Armed with Bow (Str 4); Fear 4. Damage 2D6.'},
    {'name': 'Beastman', 'weapon_skill': 4, 'ballistic_skill': 4, 'strength': 3, 'toughness': 4, 'wounds': 6, 'attacks': 1, 'move': 4, 'gold_value': 100, 'battle_level': 1, 'special_rules': 'Throw Spears (Str 3). Damage 1D6.'},
    {'name': 'Dark Elf Warrior', 'weapon_skill': 4, 'ballistic_skill': 3, 'strength': 3, 'toughness': 3, 'wounds': 6, 'attacks': 1, 'move': 5, 'gold_value': 100, 'battle_level': 1, 'special_rules': 'Armed with Crossbows (Str 4); Dodge 6+; Hate Elves. Armour 1. Damage 1D6.'},
    {'name': 'Naggaroth Black Guard', 'weapon_skill': 5, 'ballistic_skill': 3, 'strength': 4, 'toughness': 3, 'wounds': 6, 'attacks': 1, 'move': 5, 'gold_value': 150, 'battle_level': 1, 'special_rules': 'Armed with Halberds; Hate Elves. Armour 2 (T 3(5)). Damage 1D6.'},
    {'name': 'Hobgoblin', 'weapon_skill': 3, 'ballistic_skill': 4, 'strength': 3, 'toughness': 3, 'wounds': 4, 'attacks': 1, 'move': 4, 'gold_value': 50, 'battle_level': 1, 'special_rules': 'Ambush, Magic A; Break. Armour 1 (T 3(4)). Damage 1D6.'},
    {'name': 'Skeleton Swordsman', 'weapon_skill': 2, 'ballistic_skill': None, 'strength': 3, 'toughness': 3, 'wounds': 5, 'attacks': 1, 'move': 4, 'gold_value': 80, 'battle_level': 1, 'special_rules': 'Armed with Swords; Fear 5; Regenerate 1. Damage 1D6.'},
    {'name': 'Skeleton Archer', 'weapon_skill': 2, 'ballistic_skill': 5, 'strength': 3, 'toughness': 3, 'wounds': 5, 'attacks': 1, 'move': 4, 'gold_value': 80, 'battle_level': 1, 'special_rules': 'Armed with Bow (Str 3); Fear 5; Regenerate 1. Damage 1D6.'},
    {'name': 'Ghoul', 'weapon_skill': 2, 'ballistic_skill': None, 'strength': 3, 'toughness': 4, 'wounds': 4, 'attacks': 2, 'move': 4, 'gold_value': 80, 'battle_level': 1, 'special_rules': 'Break; Fear 4. Damage 1D6.'},
    {'name': 'Zombie', 'weapon_skill': 2, 'ballistic_skill': None, 'strength': 3, 'toughness': 3, 'wounds': 5, 'attacks': 1, 'move': 4, 'gold_value': 40, 'battle_level': 1, 'special_rules': 'Fear 3. Damage 1D6.'},
    {'name': 'Goblin Archer', 'weapon_skill': 2, 'ballistic_skill': 5, 'strength': 3, 'toughness': 3, 'wounds': 2, 'attacks': 1, 'move': 4, 'gold_value': 20, 'battle_level': 1, 'special_rules': 'Armed with Bow (Str 1). Damage 1D6.'},
    {'name': 'Goblin Netter', 'weapon_skill': 2, 'ballistic_skill': 5, 'strength': 3, 'toughness': 3, 'wounds': 2, 'attacks': 1, 'move': 4, 'gold_value': 35, 'battle_level': 1, 'special_rules': 'Armed with Nets. Damage Special (Net).'},
    {'name': 'Goblin Shaman', 'weapon_skill': 2, 'ballistic_skill': 5, 'strength': 3, 'toughness': 4, 'wounds': 3, 'attacks': 1, 'move': 4, 'gold_value': 280, 'battle_level': 1, 'special_rules': 'Goblin Magic 1; Magic Resistance 5+ (Ring). Damage 1D6.'},
    {'name': 'Goblin Squig Hunter', 'weapon_skill': 2, 'ballistic_skill': 5, 'strength': 3, 'toughness': 3, 'wounds': 2, 'attacks': 1, 'move': 4, 'gold_value': 25, 'battle_level': 1, 'special_rules': 'Herd Squigs. Damage 1D6.'},
    {'name': 'Wild Cave Squig', 'weapon_skill': 4, 'ballistic_skill': None, 'strength': 5, 'toughness': 3, 'wounds': 3, 'attacks': 2, 'move': 0, 'gold_value': 200, 'battle_level': 1, 'special_rules': 'Move Special; Never Pinned; Wild Squig Attack. Damage 1D6.'},
    {'name': 'Trained Cave Squig', 'weapon_skill': 4, 'ballistic_skill': None, 'strength': 5, 'toughness': 3, 'wounds': 3, 'attacks': 2, 'move': 0, 'gold_value': 200, 'battle_level': 1, 'special_rules': 'Move Special; Never Pinned. Damage 1D6.'},
    {'name': 'Skaven Stormvermin', 'weapon_skill': 4, 'ballistic_skill': 4, 'strength': 4, 'toughness': 3, 'wounds': 5, 'attacks': 1, 'move': 5, 'gold_value': 95, 'battle_level': 1, 'special_rules': 'Armour 1 (T 3(4)). Damage 1D6.'},
    {'name': 'Savage Orc', 'weapon_skill': 3, 'ballistic_skill': 4, 'strength': 3, 'toughness': 4, 'wounds': 5, 'attacks': 1, 'move': 4, 'gold_value': 65, 'battle_level': 1, 'special_rules': 'Armed with Bows (Str 4); Tattoos 6+. Damage 1D6.'},
    {'name': 'Savage Orc Shaman', 'weapon_skill': 3, 'ballistic_skill': 4, 'strength': 3, 'toughness': 5, 'wounds': 16, 'attacks': 1, 'move': 4, 'gold_value': 590, 'battle_level': 1, 'special_rules': 'Orc Magic 1; Magic Resistance 6+; Magic Weapon; Tattoos 5+. Damage 1D6.'},
    {'name': 'Rat Ogre', 'weapon_skill': 4, 'ballistic_skill': None, 'strength': 5, 'toughness': 5, 'wounds': 20, 'attacks': 2, 'move': 6, 'gold_value': 500, 'battle_level': 1, 'special_rules': 'Fear 5. Damage 2D6.'},
    {'name': 'Warhound', 'weapon_skill': 4, 'ballistic_skill': None, 'strength': 3, 'toughness': 3, 'wounds': 6, 'attacks': 1, 'move': 5, 'gold_value': 130, 'battle_level': 1, 'special_rules': 'Ambush 5+; Gang Up. Damage 1D6.'},
    {'name': 'Chaos Warrior', 'weapon_skill': 6, 'ballistic_skill': 1, 'strength': 4, 'toughness': 4, 'wounds': 12, 'attacks': 2, 'move': 4, 'gold_value': 240, 'battle_level': 2, 'special_rules': 'Armour 2 (T 4(6)). Damage 1D6.'},
    {'name': 'Gigantic Spider', 'weapon_skill': 3, 'ballistic_skill': None, 'strength': 3, 'toughness': 4, 'wounds': 20, 'attacks': 2, 'move': 5, 'gold_value': 450, 'battle_level': 2, 'special_rules': 'Fear 5; Web (1D6). Damage 2D6.'},
    {'name': 'Goblin Boss', 'weapon_skill': 3, 'ballistic_skill': 3, 'strength': 4, 'toughness': 3, 'wounds': 6, 'attacks': 2, 'move': 4, 'gold_value': 150, 'battle_level': 2, 'special_rules': 'Magic Weapon. Armour 2 (T 3(5)). Damage 1D6.'},
    {'name': 'Orc Boss', 'weapon_skill': 4, 'ballistic_skill': 3, 'strength': 4, 'toughness': 4, 'wounds': 18, 'attacks': 2, 'move': 4, 'gold_value': 330, 'battle_level': 2, 'special_rules': 'Magic Weapon. Armour 2 (T 4(6)). Damage 2D6.'},
    {'name': 'Beastman Champion', 'weapon_skill': 5, 'ballistic_skill': 3, 'strength': 4, 'toughness': 4, 'wounds': 30, 'attacks': 2, 'move': 4, 'gold_value': 610, 'battle_level': 2, 'special_rules': 'Magic Weapon; Throw Spears (Str 8). Damage 1D6/2D6 (5+).'},
    {'name': 'Minotaur Champion', 'weapon_skill': 5, 'ballistic_skill': 3, 'strength': 5, 'toughness': 4, 'wounds': 34, 'attacks': 3, 'move': 6, 'gold_value': 1100, 'battle_level': 2, 'special_rules': 'Fear 6; Magic Weapon. Damage 3D6.'},
    {'name': 'Ogre Champion', 'weapon_skill': 4, 'ballistic_skill': 4, 'strength': 5, 'toughness': 5, 'wounds': 22, 'attacks': 3, 'move': 6, 'gold_value': 800, 'battle_level': 2, 'special_rules': 'Fear 6; Magic Weapon. Damage 2D6.'},
    {'name': 'Skaven Clanrat Champion', 'weapon_skill': 4, 'ballistic_skill': 3, 'strength': 4, 'toughness': 3, 'wounds': 11, 'attacks': 2, 'move': 5, 'gold_value': 270, 'battle_level': 2, 'special_rules': 'Magic Weapon; Never Pinned. Armour 2 (T 3(5)). Damage 2D6.'},
    {'name': 'Chaos Hound', 'weapon_skill': 4, 'ballistic_skill': None, 'strength': 4, 'toughness': 4, 'wounds': 8, 'attacks': 2, 'move': 6, 'gold_value': 160, 'battle_level': 2, 'special_rules': 'Ambush 5+; Gang Up. Armour 2 (T 4(6)). Damage 1D6.'},
    {'name': 'Tomb Guardian', 'weapon_skill': 3, 'ballistic_skill': 6, 'strength': 3, 'toughness': 3, 'wounds': 15, 'attacks': 1, 'move': 4, 'gold_value': 110, 'battle_level': 2, 'special_rules': 'Fear 5; Regenerate 1. Armour 1 (T 3(4)). Damage 2D6.'},
    {'name': 'Mummy', 'weapon_skill': 3, 'ballistic_skill': None, 'strength': 4, 'toughness': 5, 'wounds': 40, 'attacks': 2, 'move': 3, 'gold_value': 450, 'battle_level': 3, 'special_rules': 'Fear 7; Tomb Rot (1D3). Damage 2D6.'},
    {'name': 'Wight', 'weapon_skill': 3, 'ballistic_skill': None, 'strength': 3, 'toughness': 4, 'wounds': 14, 'attacks': 1, 'move': 4, 'gold_value': 370, 'battle_level': 3, 'special_rules': 'Fear 7. Armour 2 (T 4(6)). Damage 2D6.'},
    {'name': 'Ghost', 'weapon_skill': 2, 'ballistic_skill': None, 'strength': 0, 'toughness': 3, 'wounds': 16, 'attacks': 1, 'move': 4, 'gold_value': 0, 'battle_level': 3, 'special_rules': 'Chill 1; Ethereal -1; Fear 6. Gold none; Damage Special.'},
    {'name': 'Wraith', 'weapon_skill': 3, 'ballistic_skill': None, 'strength': 3, 'toughness': 4, 'wounds': 30, 'attacks': 2, 'move': 4, 'gold_value': 750, 'battle_level': 4, 'special_rules': 'Chill 2; Ethereal -1; Terror 8. Damage Special.'},
    {'name': 'Troll', 'weapon_skill': 3, 'ballistic_skill': 6, 'strength': 5, 'toughness': 4, 'wounds': 30, 'attacks': 3, 'move': 6, 'gold_value': 650, 'battle_level': 3, 'special_rules': 'Fear 6; Regenerate 2; Vomit. Damage 2D6.'},
    {'name': 'Stone Troll', 'weapon_skill': 3, 'ballistic_skill': 6, 'strength': 5, 'toughness': 4, 'wounds': 25, 'attacks': 3, 'move': 6, 'gold_value': 650, 'battle_level': 3, 'special_rules': 'Fear 6; Magic Drain 6+; Regenerate 2. Damage 2D6.'},
    {'name': 'Black Orc', 'weapon_skill': 4, 'ballistic_skill': 4, 'strength': 4, 'toughness': 4, 'wounds': 7, 'attacks': 1, 'move': 4, 'gold_value': 90, 'battle_level': 2, 'special_rules': 'Armour 1 (T 4(5)). Damage 1D6.'},
    {'name': 'Chaos Champion', 'weapon_skill': 7, 'ballistic_skill': 1, 'strength': 5, 'toughness': 4, 'wounds': 15, 'attacks': 3, 'move': 4, 'gold_value': 910, 'battle_level': 3, 'special_rules': 'Magic Armour; Magic Weapon. Armour 2 (T 4(6)). Damage 1D6.'},
    {'name': 'Dark Elf Champion', 'weapon_skill': 5, 'ballistic_skill': 2, 'strength': 4, 'toughness': 3, 'wounds': 14, 'attacks': 2, 'move': 5, 'gold_value': 480, 'battle_level': 2, 'special_rules': 'Dodge 6+; Hate Elves; Magic Weapon. Armour 2 (T 3(5)). Damage 2D6.'},
    {'name': 'Skaven Assassin', 'weapon_skill': 5, 'ballistic_skill': 3, 'strength': 4, 'toughness': 3, 'wounds': 7, 'attacks': 2, 'move': 6, 'gold_value': 300, 'battle_level': 3, 'special_rules': 'Ambush A; Assassinate 6+; Dodge 5+; Weeping Blade. Damage 1D6.'},
    {'name': 'Gutter Runner', 'weapon_skill': 4, 'ballistic_skill': 3, 'strength': 4, 'toughness': 3, 'wounds': 5, 'attacks': 1, 'move': 6, 'gold_value': 120, 'battle_level': 2, 'special_rules': 'Ambush 4+. Damage 1D6.'},
    {'name': 'Plague Monk', 'weapon_skill': 3, 'ballistic_skill': 4, 'strength': 3, 'toughness': 4, 'wounds': 5, 'attacks': 1, 'move': 5, 'gold_value': 60, 'battle_level': 2, 'special_rules': 'Frenzy 5+; Weeping Blade. Damage 1D6.'},
    {'name': 'Plague Censer Bearer', 'weapon_skill': 4, 'ballistic_skill': None, 'strength': 4, 'toughness': 4, 'wounds': 4, 'attacks': 1, 'move': 5, 'gold_value': 150, 'battle_level': 3, 'special_rules': 'Armed with plague censers. Damage Special.'},
    {'name': 'Goblin Fanatic', 'weapon_skill': 2, 'ballistic_skill': 5, 'strength': 3, 'toughness': 3, 'wounds': 2, 'attacks': 1, 'move': 4, 'gold_value': 300, 'battle_level': 2, 'special_rules': 'Armed with Ball and Chain; Never Pinned. Damage Special.'},
    {'name': 'Witch Elf', 'weapon_skill': 4, 'ballistic_skill': 3, 'strength': 3, 'toughness': 3, 'wounds': 11, 'attacks': 1, 'move': 5, 'gold_value': 140, 'battle_level': 2, 'special_rules': 'Frenzy 4+; Hate Elves. Damage 1D6.'},
    {'name': 'Bloodletter', 'weapon_skill': 5, 'ballistic_skill': 2, 'strength': 4, 'toughness': 3, 'wounds': 7, 'attacks': 2, 'move': 4, 'gold_value': 200, 'battle_level': 3, 'special_rules': 'Armed with Hellblade; Daemonic -1; Fear 5. Damage 1D6.'},
    {'name': 'Daemonette', 'weapon_skill': 6, 'ballistic_skill': 2, 'strength': 4, 'toughness': 3, 'wounds': 15, 'attacks': 3, 'move': 4, 'gold_value': 300, 'battle_level': 3, 'special_rules': 'Ambush 5+; Daemonic -1; Fear 6; Magic Resistance 6+. Damage 1D6.'},
    {'name': 'Nurgling', 'weapon_skill': 3, 'ballistic_skill': 4, 'strength': 3, 'toughness': 3, 'wounds': 2, 'attacks': 2, 'move': 4, 'gold_value': 50, 'battle_level': 2, 'special_rules': 'Ambush A; Daemonic -1; Fear 4; Gang Up; Plague. Damage Special.'},
    {'name': 'Pink Horror', 'weapon_skill': 5, 'ballistic_skill': 2, 'strength': 4, 'toughness': 3, 'wounds': 8, 'attacks': 2, 'move': 4, 'gold_value': 200, 'battle_level': 3, 'special_rules': 'Daemonic -1; Fear 6; Magic Resistance 6+; Die Blue Horrors. Damage 1D6.'},
    {'name': 'Blue Horror', 'weapon_skill': 3, 'ballistic_skill': 4, 'strength': 3, 'toughness': 3, 'wounds': 4, 'attacks': 1, 'move': 4, 'gold_value': 100, 'battle_level': 3, 'special_rules': 'Daemonic -1; Fear 4; Magic Resistance 6+. Damage 1D6.'},
    {'name': 'Chaos Dwarf', 'weapon_skill': 4, 'ballistic_skill': 4, 'strength': 3, 'toughness': 4, 'wounds': 8, 'attacks': 1, 'move': 3, 'gold_value': 140, 'battle_level': 2, 'special_rules': 'Magic Resistance 6+. Armour 2 (T 4(6)). Damage 1D6/2D6 (6+).'},
    {'name': 'Orc Shaman', 'weapon_skill': 3, 'ballistic_skill': 4, 'strength': 3, 'toughness': 5, 'wounds': 16, 'attacks': 1, 'move': 4, 'gold_value': 590, 'battle_level': 2, 'special_rules': 'Orc Magic 1; Magic Resistance 6+; Magic Weapon. Damage 1D6.'},
    {'name': 'Skaven Warlock', 'weapon_skill': 3, 'ballistic_skill': 4, 'strength': 3, 'toughness': 4, 'wounds': 15, 'attacks': 1, 'move': 5, 'gold_value': 560, 'battle_level': 3, 'special_rules': 'Dodge 5+; Skaven Magic 1; Magic Dispel 6+. Damage 2D6.'},
    {'name': 'Necromancer', 'weapon_skill': 4, 'ballistic_skill': 3, 'strength': 4, 'toughness': 3, 'wounds': 25, 'attacks': 2, 'move': 4, 'gold_value': 680, 'battle_level': 3, 'special_rules': 'Necromantic Magic 1; Magic Resistance 5+; Magic Weapon; Regenerate 2. Damage 2D6.'},
    {'name': 'Harpy', 'weapon_skill': 4, 'ballistic_skill': None, 'strength': 4, 'toughness': 4, 'wounds': 22, 'attacks': 1, 'move': 6, 'gold_value': 180, 'battle_level': 2, 'special_rules': 'Claw 6+; Fly. Damage 1D6/2D6 (5+).'},
    {'name': 'Giant Scorpion', 'weapon_skill': 3, 'ballistic_skill': None, 'strength': 5, 'toughness': 6, 'wounds': 20, 'attacks': 2, 'move': 5, 'gold_value': 450, 'battle_level': 3, 'special_rules': 'Sting (2D6). Damage 2D6.'},
]

ALL_MONSTERS = CORE_MONSTERS + TABLE_MONSTERS
CORE_MONSTER_NAMES = [m["name"] for m in CORE_MONSTERS]
TABLE_MONSTER_NAMES = [m["name"] for m in TABLE_MONSTERS]
ALL_MONSTER_NAMES = [m["name"] for m in ALL_MONSTERS]
