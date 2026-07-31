"""Business services for Warhammer Quest gameplay helpers.

Currently covers the Unexpected Event deck draw (Monster vs Special).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple
import random

from django.db.models import QuerySet

from .models import EventTemplate, EventTemplateMonster

# Classic Warhammer Quest Unexpected Event deck balance (~2/3 monsters, ~1/3 events).
DEFAULT_CARD_KIND_WEIGHTS: Dict[str, int] = {
    EventTemplate.CARD_MONSTER: 65,
    EventTemplate.CARD_SPECIAL: 35,
}

DUNGEON_EVENT_TYPE_NAME = 'Dungeon Events'


@dataclass(frozen=True)
class DrawnMonsterGroup:
    """One monster type spawned by a Monster event card, with rolled count."""

    monster_id: int
    name: str
    quantity: int
    quantity_expr: str
    weapon_skill: int
    ballistic_skill: Optional[int]
    strength: int
    toughness: int
    wounds: int
    attacks: int
    move: int
    gold_value: int
    battle_level: int
    special_rules: str

    @classmethod
    def from_entry(cls, entry: EventTemplateMonster, quantity: int) -> 'DrawnMonsterGroup':
        monster = entry.monster
        return cls(
            monster_id=monster.pk,
            name=monster.name,
            quantity=quantity,
            quantity_expr=entry.quantity,
            weapon_skill=monster.weapon_skill,
            ballistic_skill=monster.ballistic_skill,
            strength=monster.strength,
            toughness=monster.toughness,
            wounds=monster.wounds,
            attacks=monster.attacks,
            move=monster.move,
            gold_value=monster.gold_value,
            battle_level=monster.battle_level,
            special_rules=monster.special_rules,
        )

    def as_dict(self) -> dict:
        return {
            'monster_id': self.monster_id,
            'name': self.name,
            'quantity': self.quantity,
            'quantity_expr': self.quantity_expr,
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


@dataclass(frozen=True)
class DrawnEvent:
    """Result of a two-step Unexpected Event draw."""

    template: EventTemplate
    card_kind: str
    monsters: Tuple[DrawnMonsterGroup, ...] = field(default_factory=tuple)
    draw_another_event: bool = False
    draw_treasure: bool = False

    @property
    def is_monster_encounter(self) -> bool:
        return self.card_kind == EventTemplate.CARD_MONSTER

    @property
    def is_special_event(self) -> bool:
        return self.card_kind == EventTemplate.CARD_SPECIAL

    def as_dict(self) -> dict:
        return {
            'template_id': self.template.pk,
            'number': self.template.number,
            'title': self.template.title,
            'card_kind': self.card_kind,
            'card_kind_label': self.template.get_card_kind_display() if self.card_kind else '',
            'description': self.template.description_copy,
            'before_form': self.template.before_form,
            'after_form': self.template.after_form,
            'draw_another_event': self.draw_another_event,
            'draw_treasure': self.draw_treasure,
            'monsters': [group.as_dict() for group in self.monsters],
        }


class EventDrawError(LookupError):
    """Raised when the Event deck cannot produce a valid card."""


def _normalize_weights(weights: Mapping[str, int]) -> Dict[str, int]:
    normalized = {
        kind: int(weight)
        for kind, weight in weights.items()
        if kind in (EventTemplate.CARD_MONSTER, EventTemplate.CARD_SPECIAL) and int(weight) > 0
    }
    if not normalized:
        raise ValueError('At least one positive card-kind weight is required')
    return normalized


def choose_card_kind(
    weights: Optional[Mapping[str, int]] = None,
    *,
    rng: Optional[random.Random] = None,
) -> str:
    """Step 1: pick MONSTER vs SPECIAL using configurable weights.

    Defaults to classic WQ proportions (~65% Monster / ~35% Special).
    """
    table = _normalize_weights(weights or DEFAULT_CARD_KIND_WEIGHTS)
    kinds: List[str] = list(table.keys())
    kind_weights: List[int] = [table[kind] for kind in kinds]
    picker = rng.choices if rng is not None else random.choices
    return picker(kinds, weights=kind_weights, k=1)[0]


def dungeon_event_queryset(
    card_kind: Optional[str] = None,
    *,
    battle_level: Optional[int] = None,
    event_type_name: str = DUNGEON_EVENT_TYPE_NAME,
) -> QuerySet:
    """Base queryset for Unexpected Event deck cards."""
    qs = EventTemplate.objects.filter(event_type__name=event_type_name)
    if card_kind:
        qs = qs.filter(card_kind=card_kind)
    else:
        qs = qs.filter(card_kind__in=[EventTemplate.CARD_MONSTER, EventTemplate.CARD_SPECIAL])
    if battle_level is not None and card_kind == EventTemplate.CARD_MONSTER:
        qs = qs.filter(monsters__battle_level=battle_level).distinct()
    return qs


def pick_random_template(queryset: QuerySet) -> EventTemplate:
    """Pick a random template from ``queryset`` (DB-side ``ORDER BY ?``)."""
    template = queryset.order_by('?').first()
    if template is None:
        raise EventDrawError('No EventTemplate matches the draw filters')
    return template


def resolve_monster_groups(
    template: EventTemplate,
    *,
    entries: Optional[Iterable[EventTemplateMonster]] = None,
) -> Tuple[DrawnMonsterGroup, ...]:
    """Roll quantities for each monster linked to ``template``."""
    if entries is None:
        entries = (
            template.monster_entries
            .select_related('monster')
            .all()
        )
    groups: List[DrawnMonsterGroup] = []
    for entry in entries:
        quantity = entry.resolve_quantity()
        if quantity <= 0:
            continue
        groups.append(DrawnMonsterGroup.from_entry(entry, quantity))
    return tuple(groups)


def build_drawn_event(template: EventTemplate) -> DrawnEvent:
    """Assemble a :class:`DrawnEvent` payload from a catalog template."""
    card_kind = template.card_kind or ''
    monsters: Tuple[DrawnMonsterGroup, ...] = ()
    if template.is_monster_event():
        monsters = resolve_monster_groups(template)
    return DrawnEvent(
        template=template,
        card_kind=card_kind,
        monsters=monsters,
        draw_another_event=template.draw_another_event,
        draw_treasure=template.draw_treasure,
    )


def draw_unexpected_event(
    *,
    weights: Optional[Mapping[str, int]] = None,
    battle_level: Optional[int] = None,
    event_type_name: str = DUNGEON_EVENT_TYPE_NAME,
    preferred_kinds: Optional[Sequence[str]] = None,
    rng: Optional[random.Random] = None,
) -> DrawnEvent:
    """Two-step Unexpected Event draw (classic Warhammer Quest).

    1. Choose card kind by weight (default 65% Monster / 35% Special).
    2. Draw a random ``EventTemplate`` of that kind from the dungeon deck.

    If the preferred kind has no cards, falls back through ``preferred_kinds``
    (default: the other kind) before raising :class:`EventDrawError`.

    For Monster events the returned payload includes rolled monster counts and
    full combat profiles needed to run the fight.
    """
    kind_weights = _normalize_weights(weights or DEFAULT_CARD_KIND_WEIGHTS)
    primary_kind = choose_card_kind(kind_weights, rng=rng)

    fallback = list(preferred_kinds) if preferred_kinds is not None else [
        kind for kind in kind_weights if kind != primary_kind
    ]
    attempt_order = [primary_kind] + [kind for kind in fallback if kind != primary_kind]

    last_error: Optional[EventDrawError] = None
    for kind in attempt_order:
        qs = dungeon_event_queryset(
            kind,
            battle_level=battle_level if kind == EventTemplate.CARD_MONSTER else None,
            event_type_name=event_type_name,
        )
        try:
            template = pick_random_template(qs)
        except EventDrawError as exc:
            last_error = exc
            continue
        return build_drawn_event(template)

    raise last_error or EventDrawError('Unexpected Event deck is empty')
