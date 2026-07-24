"""One-off fix for EventTemplate.command JSON that failed to parse."""
import json

from apps.game.models import EventTemplate


FIXES = {
    24: {  # WITCH'S CAVE
        "0": {
            "party_print": (
                "Deep in a gloomy ravine the Warriors come across the entrance to a dark cave. "
                "Inside it dwells a twisted, ugly hag who claims to be a witch. Each Warrior must "
                "pay 1D6 x 10 gold to get a single potion (roll the amount needed to buy each potion "
                "separately), and must drink it immediately."
            ),
            "each_warrior_command": "Gold-1D6*10",
        },
        "1": {
            "each_warrior_print": (
                "Your Warrior falls unconscious, writhing in agony as fire burns through him. "
                "When he awakes he feels strangely weak. He is at -1 Toughness for the duration "
                "of the next adventure."
            ),
            "each_warrior_command": "toughness-1",
        },
        "2": {
            "each_warrior_print": (
                "The potion warms your Warrior to the core. He gains +1 Wound to be added "
                "permanently to his Starting Wounds score."
            ),
            "each_warrior_command": "Wounds+1",
        },
        "3": {
            "each_warrior_print": (
                "The potion warms your Warrior to the core. He gains +1 Wound to be added "
                "permanently to his Starting Wounds score."
            ),
            "each_warrior_command": "Wounds+1",
        },
        "4": {
            "each_warrior_print": (
                "The potion warms your Warrior to the core. He gains +1 Wound to be added "
                "permanently to his Starting Wounds score."
            ),
            "each_warrior_command": "Wounds+1",
        },
        "5": {
            "each_warrior_print": (
                "A powerful heat surges through your Warrior, and he feels energy coursing through "
                "his muscles and sinews. He is at +1 Toughness for the duration of the next adventure."
            ),
            "each_warrior_command": "toughness+1",
        },
        "6": {
            "each_warrior_print": (
                "A powerful heat surges through your Warrior, and he feels energy coursing through "
                "his muscles and sinews. He is at +1 Toughness for the duration of the next adventure."
            ),
            "each_warrior_command": "toughness+1",
        },
    },
    25: {  # FAMINE
        "1": {
            "each_warrior_print": "Your Warrior gives any one item of treasure to the peasants.",
            "each_warrior_command": "treasure-1",
        },
        "2": {
            "each_warrior_print": "Your Warrior gives any one item of treasure to the peasants.",
            "each_warrior_command": "treasure-1",
        },
        "3": {
            "each_warrior_print": "Your Warrior gives 100 gold to the poor.",
            "each_warrior_command": "gold-100",
        },
        "4": {
            "each_warrior_print": "Your Warrior gives 1D6 x 10 gold to the poor.",
            "each_warrior_command": "gold-1D6*10",
        },
        "5": {
            "each_warrior_print": "Your Warrior gives 1D6 x 10 gold to the poor.",
            "each_warrior_command": "gold-1D6*10",
        },
        "6": {
            "each_warrior_print": (
                "Touched by your kindness and concern the village elder brings a carefully wrapped "
                "sword out of his house, presenting it to your Warrior in exchange for 1D6 x 50 gold.\n"
                "The magical blade is a Sword of Sharpness, and each time it is used it causes +2 Wounds "
                "on any Monster it hits.\n"
                "However, the sword can never be sold, as any attempt to get rid of it results in it "
                "mysteriously finding its way back to the village."
            ),
            "each_warrior_command": "gold-1D6*50;Sword_Of_Sharpness+1",
        },
    },
    27: {  # POOL OF DREAMS
        "1": {
            "each_warrior_print": (
                "Although he can see these reflections, the Warrior cannot make any sense of them."
            ),
        },
        "2": {
            "each_warrior_print": (
                "Although he can see these reflections, the Warrior cannot make any sense of them."
            ),
        },
        "3": {
            "each_warrior_print": (
                "Although he can see these reflections, the Warrior cannot make any sense of them."
            ),
        },
        "4": {
            "each_warrior_print": (
                "The Warrior realises that he is being granted a vision of the future! At any time "
                "during the next dungeon, he may ignore any one blow that would otherwise hit him. "
                "The Warrior recognises the blow before it hits home as the vision from the pool, "
                "and dodges away just in time. Note this on his Adventure Record sheet, crossing it "
                "off when he uses it."
            ),
        },
        "5": {
            "each_warrior_print": (
                "The Warrior realises that he is being granted a vision of the future! At any time "
                "during the next dungeon, he may ignore any one blow that would otherwise hit him. "
                "The Warrior recognises the blow before it hits home as the vision from the pool, "
                "and dodges away just in time. Note this on his Adventure Record sheet, crossing it "
                "off when he uses it."
            ),
        },
        "6": {
            "each_warrior_print": (
                "The Warrior realises that he is being granted a vision of the future! At any time "
                "during the next dungeon, he may ignore any one blow that would otherwise hit him. "
                "The Warrior recognises the blow before it hits home as the vision from the pool, "
                "and dodges away just in time. Note this on his Adventure Record sheet, crossing it "
                "off when he uses it."
            ),
        },
    },
    29: {  # LOST
        "1": {"party_command": "event+6"},
        "2": {"party_command": "event+6"},
        "3": {"party_command": "event+6"},
        "4": {"party_print": "You can check what Items your Warrior can buy in this village."},
        "5": {"party_print": "You can check what Items your Warrior can buy in this village."},
        "6": {"party_print": "You can check what Items your Warrior can buy in this village."},
    },
    30: {  # FLOOD
        "0": {
            "each_warrior_questions": {
                "ferryman": {
                    "description": (
                        "A ferryman take You across the obstruction. 20 gold. "
                        "You can continue Your trip to Settlement."
                    ),
                    "limit": "1",
                    "0": {"choice_command": "Gold-20"},
                    "1": {"choice_print": "You can continue Your trip to Settlement."},
                    "2": {"choice_print": "You can continue Your trip to Settlement."},
                    "3": {"choice_print": "You can continue Your trip to Settlement."},
                    "4": {"choice_print": "You can continue Your trip to Settlement."},
                    "5": {"choice_print": "You can continue Your trip to Settlement."},
                    "6": {"choice_print": "You can continue Your trip to Settlement."},
                },
                "next_adventure": {
                    "description": (
                        "You abandon any hope You have of reaching Your destination, in which case "
                        "You must go straight into the next adventure."
                    ),
                    "limit": "1",
                    "0": {"choice_command": "Gold-0"},
                    "1": {
                        "choice_print": (
                            "You cannot visit any Settlement. You must go straight into the next adventure."
                        ),
                    },
                    "2": {
                        "choice_print": (
                            "You cannot visit any Settlement. You must go straight into the next adventure."
                        ),
                    },
                    "3": {
                        "choice_print": (
                            "You cannot visit any Settlement. You must go straight into the next adventure."
                        ),
                    },
                    "4": {
                        "choice_print": (
                            "You cannot visit any Settlement. You must go straight into the next adventure."
                        ),
                    },
                    "5": {
                        "choice_print": (
                            "You cannot visit any Settlement. You must go straight into the next adventure."
                        ),
                    },
                    "6": {
                        "choice_print": (
                            "You cannot visit any Settlement. You must go straight into the next adventure."
                        ),
                    },
                },
            }
        }
    },
    33: {  # AMBUSH
        "1": {
            "each_warrior_print": (
                "Knocked out by a sneaky blow from behind, your Warrior awakes to find one of his "
                "weapons (determine randomly) and 2D6 x 100 gold stolen."
            ),
            "each_warrior_command": "Gold-2D6*100;item_weapon-1",
        },
        "2": {
            "each_warrior_print": (
                "Knocked out by a sneaky blow from behind, your Warrior awakes to find "
                "2D6 x 100 gold stolen."
            ),
            "each_warrior_command": "Gold-2D6*100",
        },
        "3": {
            "each_warrior_print": (
                "Knocked out by a sneaky blow from behind, your Warrior awakes to find one item of "
                "equipment stolen (determine randomly)."
            ),
            "each_warrior_command": "item_equipment-1",
        },
        "4": {
            "each_warrior_print": (
                "Fighting a glorious battle, your Warrior kills many Forest Goblins and gains "
                "1D6 x 10 gold."
            ),
            "each_warrior_command": "Gold+1D6*10",
        },
        "5": {
            "each_warrior_print": (
                "Fighting a glorious battle, your Warrior kills many Forest Goblins and gains "
                "1D6 x 50 gold."
            ),
            "each_warrior_command": "Gold+1D6*50",
        },
        "6": {
            "each_warrior_print": (
                "Fighting a glorious battle, your Warrior kills many Forest Goblins and gains "
                "1D6 x 100 gold."
            ),
            "each_warrior_command": "Gold+1D6*100",
        },
    },
    36: {  # ROCKFALL
        "0": {"each_warrior_command": "Gold-1D6*20"},
    },
    37: {  # WAGON TRAIN
        "0": {
            "each_warrior_questions": {
                "Join_convoy": {
                    "description": (
                        "The driver says that he is heading for the same destination as they are, "
                        "and if each Warrior pays him 1D6 x 10 gold they can hitch a lift, saving "
                        "them one week's travelling time."
                    ),
                    "limit": "1",
                    "0": {
                        "choice_print": "Your Warrior reach the destination one week earlier.",
                        "choice_command": "Gold-1D6*10;event-1",
                    },
                    "1": {"choice_print": "Your Warrior reach the destination one week earlier."},
                    "2": {"choice_print": "Your Warrior reach the destination one week earlier."},
                    "3": {"choice_print": "Your Warrior reach the destination one week earlier."},
                    "4": {"choice_print": "Your Warrior reach the destination one week earlier."},
                    "5": {"choice_print": "Your Warrior reach the destination one week earlier."},
                    "6": {"choice_print": "Your Warrior reach the destination one week earlier."},
                },
                "leave_convoy": {
                    "description": (
                        "Your Warrior don't want to pay for join the convoy, so He can continue "
                        "trip to the chosen destination."
                    ),
                    "limit": "1",
                    "0": {"choice_print": ""},
                    "1": {
                        "choice_print": (
                            "Your Warrior don't want to pay for join the convoy, so He can continue "
                            "trip to the chosen destination."
                        ),
                    },
                    "2": {
                        "choice_print": (
                            "Your Warrior don't want to pay for join the convoy, so He can continue "
                            "trip to the chosen destination."
                        ),
                    },
                    "3": {
                        "choice_print": (
                            "Your Warrior don't want to pay for join the convoy, so He can continue "
                            "trip to the chosen destination."
                        ),
                    },
                    "4": {
                        "choice_print": (
                            "Your Warrior don't want to pay for join the convoy, so He can continue "
                            "trip to the chosen destination."
                        ),
                    },
                    "5": {
                        "choice_print": (
                            "Your Warrior don't want to pay for join the convoy, so He can continue "
                            "trip to the chosen destination."
                        ),
                    },
                    "6": {
                        "choice_print": (
                            "Your Warrior don't want to pay for join the convoy, so He can continue "
                            "trip to the chosen destination."
                        ),
                    },
                },
            }
        }
    },
    39: {  # FALL
        "0": {
            "drawn_warrior_print": (
                "Your Warrior breaks his ankle. It takes two weeks more to reach a Settlement, "
                "and when Warrior is there, he must pay 30 gold to have his ankle healed"
            ),
            "not_drawn_warrior_print": (
                "{{ drawn_warrior }} breaks his ankle. It takes two weeks more to reach a Settlement."
            ),
            "drawn_warrior_command": "Gold-30",
            "party_print": (
                "Dragging him along slows the party down, adding two weeks to the journey"
            ),
            "party_command": "event+2",
        }
    },
    58: {  # DUEL
        "0": {
            "each_warrior_questions": {
                "Leave town immediately": {
                    "description": (
                        "Your Warrior leave the town to avoid the duel with professional duelist"
                    ),
                    "limit": "1",
                    "1": {"choice_print": "Your Warrior left the Settlement."},
                    "2": {"choice_print": "Your Warrior left the Settlement."},
                    "3": {"choice_print": "Your Warrior left the Settlement."},
                    "4": {"choice_print": "Your Warrior left the Settlement."},
                    "5": {"choice_print": "Your Warrior left the Settlement."},
                    "6": {"choice_print": "Your Warrior left the Settlement."},
                },
                "Fight!": {
                    "description": "Your Warrior takes part in the duel, and ",
                    "limit": "1",
                    "0": {"choice_command": "Gold-0"},
                    "1": {
                        "choice_print": (
                            "With a single, well-placed sword thrust your Warrior's heart is speared "
                            "and he falls to the ground, quite dead."
                        ),
                    },
                    "2": {
                        "choice_print": (
                            " The two duellists fight for hour after hour, each inflicting many light "
                            "wounds on the other. Eventually the sun goes down and the fight is "
                            "declared a draw. The duellist congratulates your Warrior on his "
                            "swordsmanship, and offers him a fine supper and the best wine at the "
                            "most expensive hotel in the Settlement."
                        ),
                    },
                    "3": {
                        "choice_print": (
                            " The two duellists fight for hour after hour, each inflicting many light "
                            "wounds on the other. Eventually the sun goes down and the fight is "
                            "declared a draw. The duellist congratulates your Warrior on his "
                            "swordsmanship, and offers him a fine supper and the best wine at the "
                            "most expensive hotel in the Settlement."
                        ),
                    },
                    "4": {
                        "choice_print": (
                            " The two duellists fight for hour after hour, each inflicting many light "
                            "wounds on the other. Eventually the sun goes down and the fight is "
                            "declared a draw. The duellist congratulates your Warrior on his "
                            "swordsmanship, and offers him a fine supper and the best wine at the "
                            "most expensive hotel in the Settlement."
                        ),
                    },
                    "5": {
                        "choice_print": (
                            "After a few minutes, your Warrior realises that he has the better of the "
                            "duellist and despatches him. On his body he finds jewels worth 2D6 x 50 "
                            "gold and a single item of treasure (take a Treasure card)."
                        ),
                        "choice_command": "Gold+2D6*50",
                    },
                    "6": {
                        "choice_print": (
                            "After a few minutes, your Warrior realises that he has the better of the "
                            "duellist and despatches him. On his body he finds jewels worth 2D6 x 50 "
                            "gold and a single item of treasure (take a Treasure card)."
                        ),
                        "choice_command": "Gold+2D6*50",
                    },
                },
            }
        }
    },
    95: {  # Too much Ale?
        "0": {"drawn_warrior_command": "Gold-1D6*100"},
    },
    96: {  # Fighting Wolverines
        "1": {
            "drawn_warrior_print": (
                " After ten minutes or so, your Warrior is just dispatching the last of the Wolverines "
                "when an enraged shout brings him out of his frenzy. It is the true owner of the beasts "
                "and he is incensed that your Warrior has killed them. He takes the pool of money as "
                "recompense for his loss."
            ),
            "not_drawn_warrior_print": (
                "{{drawn_warrior }} has killed all the beast. True owner appears and takes the pool "
                "of money as recompense for his loss."
            ),
            "drawn_warrior_command": "Gold-200",
        },
        "2": {
            "drawn_warrior_print": (
                " After a few minutes of being ripped, torn and bitten, your Warrior makes a break "
                "for it, leaping from the pit to escape. Of course, this also means that he loses "
                "the bet..."
            ),
            "not_drawn_warrior_print": (
                "{{drawn_warrior }} was almost eaten by the beasts, but he manage to escape."
            ),
            "drawn_warrior_command": "Gold-200",
        },
        "3": {
            "drawn_warrior_print": (
                " After a few minutes of being ripped, torn and bitten, your Warrior makes a break "
                "for it, leaping from the pit to escape. Of course, this also means that he loses "
                "the bet..."
            ),
            "not_drawn_warrior_print": (
                "{{drawn_warrior }} was almost eaten by the beasts, but he manage to escape."
            ),
            "drawn_warrior_command": "Gold-200",
        },
        "4": {
            "drawn_warrior_print": (
                "Your Warrior makes mincemeat of the Wolverines, dispatching the beasts with a "
                "flurry of well placed blows. The alehouse erupts into a frenzy of cheering. "
                "Your Warrior wins the wager and may claim all the money."
            ),
            "not_drawn_warrior_print": "{{drawn_warrior }} was Victoriuos!!",
            "drawn_warrior_command": "Gold+200+1D3*200",
        },
        "5": {
            "drawn_warrior_print": (
                "Your Warrior makes mincemeat of the Wolverines, dispatching the beasts with a "
                "flurry of well placed blows. The alehouse erupts into a frenzy of cheering. "
                "Your Warrior wins the wager and may claim all the money."
            ),
            "not_drawn_warrior_print": "{{drawn_warrior }} was Victoriuos!!",
            "drawn_warrior_command": "Gold+200+1D3*200",
        },
        "6": {
            "drawn_warrior_print": (
                "Your Warrior makes mincemeat of the Wolverines, dispatching the beasts with a "
                "flurry of well placed blows. The alehouse erupts into a frenzy of cheering. "
                "Your Warrior wins the wager and may claim all the money."
            ),
            "not_drawn_warrior_print": "{{drawn_warrior }} was Victoriuos!!",
            "drawn_warrior_command": "Gold+200+1D3*200",
        },
    },
    97: {  # Magical Potion
        "1": {
            "drawn_warrior_print": (
                " The foul liquid tastes like whatever it was that Squint Eyed Rogar last drank, "
                "and has no noticeable effect other than to induce a mysterious nausea."
            ),
        },
        "2": {
            "drawn_warrior_print": (
                " The foul liquid tastes like whatever it was that Squint Eyed Rogar last drank, "
                "and has no noticeable effect other than to induce a mysterious nausea."
            ),
        },
        "3": {
            "drawn_warrior_print": (
                "As the mild saline solution trickles down your Warrior's throat, he realises he's "
                "been had. A blind, raging fury overcomes him and he goes berserk, hacking and "
                "slashing at his enemies for the rest of this combat. Your Warrior is now subject "
                "to all the normal rules for being berserk (see the Barbarian's Warrior card). He "
                "remains berserk until all the Monsters in the room are dead. Perhaps it was "
                "magical after all..."
            ),
        },
        "4": {
            "drawn_warrior_print": (
                "As the mild saline solution trickles down your Warrior's throat, he realises he's "
                "been had. A blind, raging fury overcomes him and he goes berserk, hacking and "
                "slashing at his enemies for the rest of this combat. Your Warrior is now subject "
                "to all the normal rules for being berserk (see the Barbarian's Warrior card). He "
                "remains berserk until all the Monsters in the room are dead. Perhaps it was "
                "magical after all..."
            ),
        },
        "5": {
            "drawn_warrior_print": (
                "As the mild saline solution trickles down your Warrior's throat, he realises he's "
                "been had. A blind, raging fury overcomes him and he goes berserk, hacking and "
                "slashing at his enemies for the rest of this combat. Your Warrior is now subject "
                "to all the normal rules for being berserk (see the Barbarian's Warrior card). He "
                "remains berserk until all the Monsters in the room are dead. Perhaps it was "
                "magical after all..."
            ),
        },
        "6": {
            "drawn_warrior_print": (
                "Your belief in the strength of the potion makes you feel so much better that you "
                "immediately regain 1D6 Wounds."
            ),
            "drawn_warrior_command": "heal_wounds+1D6",
        },
    },
    101: {  # Slaughterhouse Singers
        "1": {"drawn_warrior_print": "Nothing happens. The Monster still standing."},
        "2": {"drawn_warrior_print": "Nothing happens. The Monster still standing."},
        "3": {"drawn_warrior_print": "Nothing happens. The Monster still standing."},
        "4": {"drawn_warrior_print": "Nothing happens. The Monster still standing."},
        "5": {"drawn_warrior_print": "Monster falls dead from fright."},
        "6": {"drawn_warrior_print": "Monster falls dead from fright."},
    },
    102: {  # Mammoth Drinking Session
        "0": {"drawn_warrior_command": "Gold+(1D6+2)*100"},
    },
}


def run():
    updated = []
    for pk, data in FIXES.items():
        et = EventTemplate.objects.get(pk=pk)
        payload = json.dumps(data, ensure_ascii=False)
        json.loads(payload)  # sanity
        et.command = payload
        et.save(update_fields=["command"])
        updated.append((pk, et.title))

    remaining = []
    for e in EventTemplate.objects.exclude(command__in=["", "{}", None]).order_by("id"):
        try:
            json.loads(e.command)
        except Exception as ex:
            remaining.append((e.id, e.title, str(ex)))

    print("UPDATED", len(updated))
    for row in updated:
        print(" ", row)
    print("REMAINING_BAD", remaining)


if __name__ == "__main__":
    run()
