"""Dungeon Event template commands.

Convention:
- "some Warrior" / "lowest score" → drawn_warrior (random party member)
- each Warrior rolls own 1D6 → keys "1".."6" with each_warrior_* (no party_table)
- one party 1D6 decides outcome for all → "0": {"party_table": true} + keys "1".."6"
"""

DRAW_ANOTHER = {
    "party_print": "Draw another Event card immediately.",
    "party_command": "dungeon_event+1",
}

DRAW_ON_1_TO_3 = {
    "1": {**DRAW_ANOTHER},
    "2": {**DRAW_ANOTHER},
    "3": {**DRAW_ANOTHER},
    "4": {"party_print": "No further Event is drawn."},
    "5": {"party_print": "No further Event is drawn."},
    "6": {"party_print": "No further Event is drawn."},
}


def _bf(*parts):
    return "\n\n".join(parts)


DUNGEON_EVENT_UPDATES = {
    72: {  # CAVE IN
        "before_form": _bf(
            "As the Warriors enter this area of the cave system, the floor shudders, the walls "
            "splinter and huge chunks of masonry fall from the roof — the dungeon is caving in!",
            "Place the Cave-in marker in the board section where this Event was triggered. All exits "
            "except the one the Warriors entered by are blocked. Any Warriors still in this board "
            "section at the end of the next turn are crushed and killed. Warriors escaping are not "
            "subject to pinning in this room. The room is now impassable.",
            "If this Event occurs in the first room, ignore it and draw another Event card immediately.",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "party_print": (
                    "Resolve the cave-in on the board. If this was the first room, ignore this Event "
                    "and treat the drawn card below as the replacement."
                ),
                "party_command": "dungeon_event+1",
            },
        },
    },
    73: {  # DEAD BODY
        "before_form": _bf(
            "The Warriors find a dead Barbarian, lying in a pool of blood. Clutched tightly to his "
            "chest is a bag.",
            "{{ drawn_warrior_name }} is chosen to take the bag from the body and open it.",
            "{{ party_print }}",
            "{{ drawn_warrior_print }}",
            "{{ each_warrior_print }}",
        ),
        "command": {
            "0": {
                "party_table": True,
                "party_print": "The bag is opened...",
                "party_command": "dungeon_event+1",
            },
            "1": {
                "party_print": "Poison Gas! Every Warrior on this board section is caught in the cloud.",
                "each_warrior_print": "You take 1D6 Wounds with no modifiers for Toughness or armour. The bag is empty.",
                "each_warrior_command": "Wounds-1D6",
            },
            "2": {
                "party_print": "Trap! A spear shoots out of the wall.",
                "drawn_warrior_print": "The spear hits you for 2D6 Wounds. The bag turns out to be empty.",
                "drawn_warrior_command": "Wounds-2D6",
            },
            "3": {
                "party_print": "Trap! A spear shoots out of the wall.",
                "drawn_warrior_print": "The spear hits you for 2D6 Wounds. The bag turns out to be empty.",
                "drawn_warrior_command": "Wounds-2D6",
            },
            "4": {
                "party_print": "Treasure!",
                "drawn_warrior_print": "The bag contains gold for you alone.",
                "drawn_warrior_command": "Gold+1D6*100",
            },
            "5": {
                "party_print": "Treasure!",
                "drawn_warrior_print": "The bag contains gold for you alone.",
                "drawn_warrior_command": "Gold+1D6*100",
            },
            "6": {
                "party_print": "Treasure!",
                "drawn_warrior_print": "The bag contains gold for you alone.",
                "drawn_warrior_command": "Gold+1D6*100",
            },
        },
    },
    74: {  # DYING DWARF
        "before_form": _bf(
            "Slumped against the wall the Warriors find a dying Dwarf prospector, stuffed with Orc "
            "arrows. When he sees that they are not Orcs he calms down and gives them a key.",
            "With his dying breath he says: \"This is the key to the portcullis. Without it you will "
            "never get through.\"",
            "{{ drawn_warrior_name }} takes the key. Note this on their Adventure Record sheet.",
            "{{ drawn_warrior_print }}",
        ),
        "command": {
            "0": {
                "drawn_warrior_print": "You now carry the portcullis key.",
            },
        },
    },
    75: {  # ENCOUNTER - WARRIOR
        "before_form": _bf(
            "The Warriors meet a lone mercenary, the only survivor of another band. He describes some "
            "of the dungeon layout before heading for the way out.",
            "You may take the next three cards from the Dungeon deck and re-order them as you like.",
            "{{ party_print }}",
        ),
        "command": {
            "0": {"party_table": True},
            **DRAW_ON_1_TO_3,
        },
    },
    76: {  # SNEAKY GIT
        "before_form": _bf(
            "A Snotling runs out of the darkness and tags along behind the Warriors, hoping to steal "
            "treasure. While he is with them they may all move an extra square each turn.",
            "Whenever an Unexpected Event that reveals Monsters occurs, roll 1D6: 1–3 he warns the "
            "Monsters (they attack immediately); 4–6 he warns the Warriors (+1 Attack each in the "
            "first round).",
            "If the Warriors kill him, roll twice on the Monster Table one higher than the party's "
            "Battle-level. At the end of each turn roll 2D6; on double 1 or 2 he sneaks off forever.",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "party_print": "The Snotling joins the party. Track his special rules on the board.",
            },
        },
    },
    77: {  # GHOST
        "before_form": _bf(
            "A dim light flickers into the shadowy form of a ghostly man. He beckons the Warriors on "
            "and they are compelled to follow him.",
            "{{ party_print }}",
            "{{ drawn_warrior_print }}",
            "{{ each_warrior_print }}",
        ),
        "command": {
            "0": {"party_table": True},
            "1": {
                "party_print": "The Ghost leads the Warriors into a pit trap!",
                "each_warrior_print": "You take 2D6 Wounds with no modifiers for Toughness or armour. "
                "It takes three turns to climb out without a rope, but only one turn with it.",
                "each_warrior_command": "Wounds-2D6",
            },
            "2": {
                "party_print": "A trip wire fires a poison dart.",
                "drawn_warrior_print": "The dart hits your leg for 1D6 Wounds (no Toughness/armour).",
                "drawn_warrior_command": "Wounds-1D6",
            },
            "3": {
                "party_print": "A trip wire fires a poison dart.",
                "drawn_warrior_print": "The dart hits your leg for 1D6 Wounds (no Toughness/armour).",
                "drawn_warrior_command": "Wounds-1D6",
            },
            "4": {
                "party_print": "The Ghost leads the Warriors to a concealed pile of gold!",
                "each_warrior_print": "You find gold in the alcove.",
                "each_warrior_command": "Gold+1D6*50",
            },
            "5": {
                "party_print": "The Ghost leads the Warriors to a concealed pile of gold!",
                "each_warrior_print": "You find gold in the alcove.",
                "each_warrior_command": "Gold+1D6*50",
            },
            "6": {
                "party_print": "The Ghost leads the Warriors to a concealed pile of gold!",
                "each_warrior_print": "You find gold in the alcove.",
                "each_warrior_command": "Gold+1D6*50",
            },
        },
    },
    78: {  # PRISONERS
        "before_form": _bf(
            "Three prisoners emerge from the shadows and beg for protection, claiming to be wealthy "
            "merchants who will pay once free.",
            "If they join, note it on the leader's sheet. In combat they hide. If the Warriors survive "
            "and escort them to a Settlement, resolve payment there (1: pay 1D6×100 gold each as "
            "\"kidnappers\"; 2–6: gain 2D6×100 gold each).",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "party_table": True,
                "party_options": {
                    "Let them join": {
                        "description": "Allow the prisoners to tag along with the party.",
                        "option_command": "",
                    },
                    "Refuse them": {
                        "description": "Send the prisoners away into the darkness.",
                        "option_command": "",
                    },
                },
            },
            **DRAW_ON_1_TO_3,
        },
    },
    79: {  # STRANGER
        "before_form": _bf(
            "The Warriors meet a mysterious cloaked stranger who asks what their business is.",
            "{{ party_print }}",
            "{{ drawn_warrior_print }}",
            "{{ each_warrior_print }}",
        ),
        "command": {
            "0": {
                "party_options": {
                    "Attack the stranger": {
                        "description": "The Warriors draw weapons and attack.",
                        "option_command": "",
                    },
                    "Hear him out": {
                        "description": "Listen to his warning and let him leave.",
                        "option_command": "",
                    },
                },
                "party_print": (
                    "If you attacked: on 1–3 he wounds each Warrior for 2D6 and vanishes; on 4–6 he "
                    "flees dropping a bag (1: explodes for 2D6 Wounds each; 2–6: healing herbs "
                    "heal_wounds+4D6 on one Warrior). If you did not attack, he warns you — then each "
                    "Warrior rolling 1 loses one random treasure item. No Treasure card for this Event."
                ),
            },
            "1": {
                "each_warrior_print": "As payment for his advice, the stranger steals a treasure item from you!",
                "each_warrior_command": "treasure-1",
            },
            "2": {},
            "3": {},
            "4": {},
            "5": {},
            "6": {},
        },
    },
    80: {  # GOLD DIGGER
        "before_form": _bf(
            "The Warriors meet an aged Dwarf with a huge sack. He demands 100 gold from each Warrior "
            "to pass, claiming to be Lord of the Dungeon. The only ways past are to pay or kill him.",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "party_options": {
                    "Pay 100 gold each": {
                        "description": "Each Warrior pays 100 gold and the party may continue.",
                        "option_command": "party_gold-100",
                    },
                    "Kill the Dwarf": {
                        "description": (
                            "Attack the old prospector. He curses the party as he dies — each Warrior "
                            "rolls 1D6; on a 1 Toughness is permanently reduced by -1."
                        ),
                        "option_command": "gold_digger_curse",
                    },
                },
                "party_table": True,
            },
            **DRAW_ON_1_TO_3,
        },
    },
    81: {  # NURGLE'S ROT
        "before_form": _bf(
            "A slumped, cowled figure crawls toward the Warriors, calling for help.",
            "{{ drawn_warrior_name }} rushes to help — and finds a plague-ridden corpse!",
            "{{ drawn_warrior_print }}",
            "{{ each_warrior_print }}",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "party_table": True,
                "party_command": "dungeon_event+1",
                "party_print": "Draw another Event card immediately.",
                "drawn_warrior_print": (
                    "You caught Nurgle's Rot! Toughness -1 now. Until cured (3 healing potions or "
                    "2,000 gold in a Settlement), further Unexpected Events may reduce another "
                    "characteristic by -1. If any characteristic reaches 0, you die."
                ),
                "drawn_warrior_command": "Toughness-1",
            },
        },
    },
    82: {  # SCORPION SWARM
        "before_form": _bf(
            "A scuttling mass of scorpions engulfs one of the Warriors.",
            "{{ drawn_warrior_name }} is attacked by the swarm of 12 scorpions!",
            "{{ drawn_warrior_print }}",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "party_table": True,
                "drawn_warrior_print": (
                    "You roll damage (1D6 + Strength) to kill scorpions (5 gold each). Remaining "
                    "scorpions inflict 1 Wound each (no Toughness/armour)."
                ),
                "drawn_warrior_command": "scorpion_swarm",
            },
            **DRAW_ON_1_TO_3,
        },
    },
    83: {  # SNAKES (keep existing logic; refresh before_form)
        "before_form": _bf(
            "Without warning, hundreds of snakes suddenly drop into the room through carefully "
            "concealed holes in the roof. Each Warrior is quickly covered in a writhing mass of "
            "venomous serpents.",
            "{{ each_warrior_print }}",
            "{{ party_print }}",
        ),
        "command": {
            "0": {**DRAW_ANOTHER},
            "1": {
                "each_warrior_print": (
                    "The snakes bite through your armour. You suffer 1D6 Wounds (no Toughness/armour). "
                    "You cannot act for the rest of the turn; Monsters get +1 to hit you. At the start "
                    "of the next Warriors' Phase, roll on this table again."
                ),
                "each_warrior_command": "Wounds-1D6",
            },
            "2": {
                "each_warrior_print": (
                    "The snakes bite through your armour. You suffer 1D6 Wounds (no Toughness/armour). "
                    "You cannot act for the rest of the turn; Monsters get +1 to hit you. At the start "
                    "of the next Warriors' Phase, roll on this table again."
                ),
                "each_warrior_command": "Wounds-1D6",
            },
            "3": {
                "each_warrior_print": (
                    "The snakes bite you for 1D6 Wounds (no Toughness/armour). You free yourself and "
                    "slash the serpents to pieces."
                ),
                "each_warrior_command": "Wounds-1D6",
            },
            "4": {
                "each_warrior_print": (
                    "The snakes bite you for 1D6 Wounds (no Toughness/armour). You free yourself and "
                    "slash the serpents to pieces."
                ),
                "each_warrior_command": "Wounds-1D6",
            },
            "5": {
                "each_warrior_print": (
                    "You nimbly avoid the snakes, killing them as they fall. The attack has no effect."
                ),
            },
            "6": {
                "each_warrior_print": (
                    "You nimbly avoid the snakes, killing them as they fall. The attack has no effect."
                ),
            },
        },
    },
    84: {  # TRAP (generic) — OCR was broken; sensible reconstruction
        "before_form": _bf(
            "A trap is sprung!",
            "{{ drawn_warrior_name }} set it off.",
            "{{ party_print }}",
            "{{ drawn_warrior_print }}",
            "{{ each_warrior_print }}",
        ),
        "command": {
            "0": {"party_table": True},
            "1": {
                "party_print": "There is a loud explosion — fire and smoke fill the room!",
                "each_warrior_print": "You take 1D6 Wounds with no modifiers for Toughness or armour.",
                "each_warrior_command": "Wounds-1D6",
            },
            "2": {
                "party_print": "A pit opens in the floor!",
                "drawn_warrior_print": (
                    "You plummet onto rock for 2D6 Wounds. Escape only with a rope or Levitation spell."
                ),
                "drawn_warrior_command": "Wounds-2D6",
            },
            "3": {
                "party_print": "A pit opens in the floor!",
                "drawn_warrior_print": (
                    "You plummet onto rock for 2D6 Wounds. Escape only with a rope or Levitation spell."
                ),
                "drawn_warrior_command": "Wounds-2D6",
            },
            "4": {
                "party_print": "A pit opens in the floor!",
                "drawn_warrior_print": (
                    "You plummet onto rock for 2D6 Wounds. Escape only with a rope or Levitation spell."
                ),
                "drawn_warrior_command": "Wounds-2D6",
            },
            "5": {
                "party_print": "A stone slab slides back, revealing gems and gold! Draw one Treasure card.",
            },
            "6": {
                "party_print": "A stone slab slides back, revealing gems and gold! Draw one Treasure card.",
            },
            # draw another on 1-3 — merge into above for 1-3
        },
    },
    85: {  # SPIKED PIT
        "before_form": _bf(
            "A spiked pit yawns open!",
            "{{ drawn_warrior_name }} tumbles in, taking {{ roll_4D6 }} Wounds on the stakes below. Escape only "
            "with a rope or Levitate; otherwise they remain trapped.",
            "{{ drawn_warrior_print }}",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "party_table": True,
                "drawn_warrior_print": "You hit the spikes hard and take 4D6 Wounds.",
                "drawn_warrior_command": "Wounds-4D6",
            },
            **DRAW_ON_1_TO_3,
        },
    },
    86: {  # POISON DART
        "before_form": _bf(
            "A poison dart trap clicks!",
            "{{ drawn_warrior_name }} is hit in the arm.",
            "{{ drawn_warrior_print }}",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "party_table": True,
                "drawn_warrior_print": "The dart inflicts 1D6 Wounds (no armour modifier).",
                "drawn_warrior_command": "Wounds-1D6",
            },
            "1": {
                "drawn_warrior_print": "Poison enters your system! Strength -1 for the rest of the adventure (or until a healing potion).",
                "drawn_warrior_command": "Strength-1",
                **DRAW_ANOTHER,
            },
            "2": {
                "drawn_warrior_print": "Poison enters your system! Strength -1 for the rest of the adventure (or until a healing potion).",
                "drawn_warrior_command": "Strength-1",
                **DRAW_ANOTHER,
            },
            "3": {
                "drawn_warrior_print": "Poison enters your system! Strength -1 for the rest of the adventure (or until a healing potion).",
                "drawn_warrior_command": "Strength-1",
                **DRAW_ANOTHER,
            },
            "4": {"party_print": "The poison fails to take hold. No further Event is drawn."},
            "5": {"party_print": "The poison fails to take hold. No further Event is drawn."},
            "6": {"party_print": "The poison fails to take hold. No further Event is drawn."},
        },
    },
    87: {  # STONE BLOCK
        "before_form": _bf(
            "A stone-block trap is triggered!",
            "{{ drawn_warrior_name }} is in its path.",
            "{{ party_print }}",
            "{{ drawn_warrior_print }}",
        ),
        "command": {
            "0": {"party_table": True},
            "1": {
                "party_print": "A huge stone block crashes down!",
                "drawn_warrior_print": (
                    "You are trapped and take 5D6 Wounds. Others must spend turns rolling "
                    "1D6+Strength each; total 20+ frees you."
                ),
                "drawn_warrior_command": "Wounds-5D6",
            },
            "2": {
                "party_print": "A huge stone block crashes down!",
                "drawn_warrior_print": (
                    "You are trapped and take 5D6 Wounds. Others must spend turns rolling "
                    "1D6+Strength each; total 20+ frees you."
                ),
                "drawn_warrior_command": "Wounds-5D6",
            },
            "3": {
                "party_print": "A huge stone block crashes down!",
                "drawn_warrior_print": (
                    "You are trapped and take 5D6 Wounds. Others must spend turns rolling "
                    "1D6+Strength each; total 20+ frees you."
                ),
                "drawn_warrior_command": "Wounds-5D6",
            },
            "4": {
                "party_print": "The stone block falls — but misses!",
                "drawn_warrior_print": "You step aside in time. The trap has no effect.",
            },
            "5": {
                "party_print": "The stone block falls — but misses!",
                "drawn_warrior_print": "You step aside in time. The trap has no effect.",
            },
            "6": {
                "party_print": "The stone block falls — but misses!",
                "drawn_warrior_print": "You step aside in time. The trap has no effect.",
            },
        },
    },
    88: {  # PARALYSIS SPELL
        "before_form": _bf(
            "A paralysis trap fires a bolt of power!",
            "{{ drawn_warrior_name }} is paralysed for 1D6 turns — they can do nothing and Monsters "
            "will not attack them.",
            "{{ drawn_warrior_print }}",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "drawn_warrior_print": "You are frozen like a statue for 1D6 turns. Note the duration.",
                **DRAW_ANOTHER,
            },
        },
    },
    89: {  # GASEOUS EXPLOSION
        "before_form": _bf(
            "A gas trap floods the room!",
            "{{ drawn_warrior_name }} set it off. Each Warrior tries to hold their breath.",
            "{{ each_warrior_print }}",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "party_print": "{{ drawn_warrior_name }} triggered the gas trap.",
            },
            "1": {
                "each_warrior_print": "The gas overwhelms you! Toughness and Strength -1 for 2D6 turns (note duration).",
                "each_warrior_command": "Toughness-1;Strength-1",
            },
            "2": {
                "each_warrior_print": "The gas overwhelms you! To hit rolls -1 for the rest of the adventure (note it).",
            },
            "3": {
                "each_warrior_print": "The gas overwhelms you! You suffer 1D6 Wounds (no Toughness/armour).",
                "each_warrior_command": "Wounds-1D6",
            },
            "4": {
                "each_warrior_print": "You hold your breath until the gas dissipates. No ill effects.",
            },
            "5": {
                "each_warrior_print": "You hold your breath until the gas dissipates. No ill effects.",
            },
            "6": {
                "each_warrior_print": "You hold your breath until the gas dissipates. No ill effects.",
            },
        },
    },
    90: {  # LIGHTNING BOLT
        "before_form": _bf(
            "A lightning-bolt trap arcs from the ceiling!",
            "{{ drawn_warrior_name }} is struck for 2D6 Wounds (no armour modifier).",
            "The bolt may arc to others until it earths (board resolution / further rolls).",
            "{{ drawn_warrior_print }}",
            "{{ party_print }}",
        ),
        "command": {
            "0": {
                "drawn_warrior_print": "Lightning burns through you!",
                "drawn_warrior_command": "Wounds-2D6",
                "party_print": (
                    "After resolving the first hit, roll 1D6: 1–3 the bolt arcs to another random "
                    "Warrior for the same damage; 4–6 it earths. Repeat until it earths or all are hit."
                ),
            },
        },
    },
    91: {  # OLD BONES
        "before_form": _bf(
            "The floor is littered with bones and skulls, gold glinting underneath.",
            "{{ party_print }}",
            "{{ drawn_warrior_print }}",
            "{{ each_warrior_print }}",
        ),
        "command": {
            "0": {"party_table": True},
            "1": {
                "party_print": "Trap! Cackling laughter and a magical bolt!",
                "drawn_warrior_print": "The bolt hits you for 1D6 Wounds (no Toughness/armour).",
                "drawn_warrior_command": "Wounds-1D6",
            },
            "2": {
                "party_print": "Illusion! The bones and gold vanish.",
                **DRAW_ANOTHER,
            },
            "3": {
                "party_print": "Illusion! The bones and gold vanish.",
                **DRAW_ANOTHER,
            },
            "4": {
                "party_print": "Real gold among the bones!",
                "each_warrior_print": "You find gold.",
                "each_warrior_command": "Gold+1D6*10",
                **DRAW_ANOTHER,
            },
            "5": {
                "party_print": "Real gold among the bones!",
                "each_warrior_print": "You find gold.",
                "each_warrior_command": "Gold+1D6*10",
                **DRAW_ANOTHER,
            },
            "6": {
                "party_print": "A rich cache! Draw one Treasure card as well.",
                "each_warrior_print": "You find a larger share of gold.",
                "each_warrior_command": "Gold+2D6*10",
            },
        },
    },
    92: {  # LOCKED DOOR
        "before_form": _bf(
            "The next door is locked with a huge padlock. A Warrior with lock picks may try each turn "
            "(roll 1D6; open on 6) and can do nothing else while picking. If it cannot be opened, "
            "the Warriors must turn back.",
            "{{ party_print }}",
        ),
        "command": {
            "0": {**DRAW_ANOTHER},
        },
    },
    93: {  # PORTCULLIS
        "before_form": _bf(
            "Once all Warriors have entered this board section, a portcullis slams shut behind them. "
            "They may only retrace their steps if they have the key (see Encounter — Dying Dwarf).",
            "Place the portcullis marker across the doorway they entered by.",
            "{{ party_print }}",
        ),
        "command": {
            "0": {**DRAW_ANOTHER},
        },
    },
}


# Fix TRAP 84: add draw-another on results 1-3
for _k in ("1", "2", "3"):
    DUNGEON_EVENT_UPDATES[84]["command"][_k] = {
        **DUNGEON_EVENT_UPDATES[84]["command"][_k],
        **DRAW_ANOTHER,
    }
