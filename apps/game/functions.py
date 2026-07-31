from .models import Character, Event, EventTemplate, CharacterParameter, Parameter
from random import randint, randrange
from django.db.models import Q, Sum
from django.template import Template, Context
import ast
import json
import operator
import re
import logging

logger = logging.getLogger('error_logger')

_DICE_RE = re.compile(r'(\d+)D(\d+)', re.IGNORECASE)
_GOLD_CMD_RE = re.compile(r'^gold([+/=-])(.+)$', re.IGNORECASE)
_EVENT_CMD_RE = re.compile(r'^event([+-])(.+)$', re.IGNORECASE)
_DUNGEON_EVENT_CMD_RE = re.compile(r'^dungeon_event([+-])(.+)$', re.IGNORECASE)
_WOUNDS_CMD_RE = re.compile(r'^(?:heal_)?wounds([+/=-])(.+)$', re.IGNORECASE)
_STAT_CMD_RE = re.compile(
    r'^(toughness|strength|strenght|weapon_skill|ballistic_skill|initiative|attacks|luck|willpower|move|movement)'
    r'([+/=-])(.+)$',
    re.IGNORECASE,
)
_ITEM_TREASURE_CMD_RE = re.compile(r'^(?:item_treasure|treasure)([+-])(.+)$', re.IGNORECASE)
_PARTY_GOLD_CMD_RE = re.compile(r'^party_gold([+/=-])(.+)$', re.IGNORECASE)
_SCORPION_CMD_RE = re.compile(r'^scorpion_swarm$', re.IGNORECASE)
_GOLD_DIGGER_CURSE_RE = re.compile(r'^gold_digger_curse$', re.IGNORECASE)
_STAT_SHORT = {
    'toughness': 'T',
    'strength': 'S',
    'strenght': 'S',
    'weapon_skill': 'WS',
    'ballistic_skill': 'BS',
    'initiative': 'I',
    'attacks': 'A',
    'luck': 'L',
    'willpower': 'WP',
    'move': 'M',
    'movement': 'M',
}
_AST_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def Roll(command):
    match = re.search(r'(\d+)D(\d+)([-+]\d+)?', command)
    if match:
        no_of_dices = int(match.group(1))
        sides_of_dice = int(match.group(2))
        try:
            modifier = int(match.group(3))
        except TypeError:
            modifier = 0
        result = sum(randint(1, sides_of_dice) for i in range(no_of_dices)) + modifier
        if result < no_of_dices:
            result = no_of_dices
        if result > sides_of_dice * no_of_dices:
            result = sides_of_dice * no_of_dices
        return result
    return None


def _eval_ast(node):
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return int(node.value)
        raise ValueError('unsupported constant')
    if isinstance(node, ast.Num):  # pragma: no cover - py<3.8
        return int(node.n)
    if isinstance(node, ast.BinOp):
        return _AST_OPS[type(node.op)](_eval_ast(node.left), _eval_ast(node.right))
    if isinstance(node, ast.UnaryOp):
        return _AST_OPS[type(node.op)](_eval_ast(node.operand))
    raise ValueError('unsupported expression')


def eval_amount(expr):
    """Evaluate expressions like '40', '1D6*10', '200+1D3*200'."""
    if expr is None:
        return 0
    text = str(expr).strip()
    if not text:
        return 0

    def repl(match):
        return str(Roll(match.group(0)))

    replaced = _DICE_RE.sub(repl, text)
    if not re.fullmatch(r'[\d\s+\-*/()]+', replaced):
        raise ValueError('invalid amount expression: {!r}'.format(expr))
    return int(_eval_ast(ast.parse(replaced, mode='eval')))


def _split_commands(raw):
    if not raw:
        return []
    if isinstance(raw, list):
        return [part.strip() for part in raw if str(part).strip()]
    return [part.strip() for part in str(raw).split(';') if part.strip()]


def execute_event_commands(character, commands, reason='Event'):
    """Apply event command tokens (gold+/-, event+/-, ...)."""
    for raw in _split_commands(commands):
        try:
            _execute_single_command(character, raw, reason)
        except Exception:
            logger.exception('Failed to execute event command %r for %s', raw, character)


def _execute_single_command(character, command, reason):
    cmd = command.strip()
    if not cmd:
        return

    gold_match = _GOLD_CMD_RE.match(cmd)
    if gold_match:
        op, expr = gold_match.group(1), gold_match.group(2)
        why = '{}: {}'.format(reason, cmd)
        current = character.get_current_gold() or 0
        if op == '+':
            character.add_gold(eval_amount(expr), why)
        elif op == '-':
            character.remove_gold(eval_amount(expr), why)
        elif op == '=':
            target = eval_amount(expr)
            if current > target:
                character.remove_gold(current - target, why)
            elif current < target:
                character.add_gold(target - current, why)
        elif op == '/':
            divisor = eval_amount(expr)
            if divisor <= 0:
                raise ValueError('gold divisor must be > 0')
            keep = current // divisor
            if current > keep:
                character.remove_gold(current - keep, why)
        return

    event_match = _EVENT_CMD_RE.match(cmd)
    if event_match:
        # Party travel modifiers must run once for the party (leader only).
        if character.leader_id != character.pk:
            return
        delta = eval_amount(event_match.group(2))
        if event_match.group(1) == '-':
            delta = -delta
        _apply_party_event_delta(character, delta)
        return

    dungeon_event_match = _DUNGEON_EVENT_CMD_RE.match(cmd)
    if dungeon_event_match:
        if character.leader_id != character.pk:
            return
        delta = eval_amount(dungeon_event_match.group(2))
        if dungeon_event_match.group(1) == '-':
            delta = -delta
        if delta > 0:
            for _ in range(delta):
                roll_unexpected_dungeon_event(character)
        elif delta < 0:
            to_cancel = list(
                Event.objects.filter(
                    character=character,
                    done=False,
                    template__event_type__name='Dungeon Events',
                ).order_by('-created')[: abs(delta)]
            )
            for pending in to_cancel:
                root_id = pending.leader_event_id or pending.pk
                Event.objects.filter(Q(pk=root_id) | Q(leader_event_id=root_id)).update(done=True)
        return

    wounds_match = _WOUNDS_CMD_RE.match(cmd)
    if wounds_match:
        op, expr = wounds_match.group(1), wounds_match.group(2)
        why = '{}: {}'.format(reason, cmd)
        amount = eval_amount(expr)
        if op == '+':
            _apply_wounds_delta(character, amount, why)
        elif op == '-':
            _apply_wounds_delta(character, -amount, why)
        elif op == '=':
            current = (
                CharacterParameter.objects
                .filter(character=character, parameter__short_name='W')
                .aggregate(total=Sum('value'))['total']
            ) or 0
            _apply_wounds_delta(character, amount - current, why)
        return

    stat_match = _STAT_CMD_RE.match(cmd)
    if stat_match:
        alias, op, expr = stat_match.group(1), stat_match.group(2), stat_match.group(3)
        short = _STAT_SHORT[alias.lower()]
        why = '{}: {}'.format(reason, cmd)
        amount = eval_amount(expr)
        if op == '+':
            _apply_stat_delta(character, short, amount, why)
        elif op == '-':
            _apply_stat_delta(character, short, -amount, why)
        elif op == '=':
            current = (
                CharacterParameter.objects
                .filter(character=character, parameter__short_name=short)
                .aggregate(total=Sum('value'))['total']
            ) or 0
            _apply_stat_delta(character, short, amount - current, why)
        return

    treasure_match = _ITEM_TREASURE_CMD_RE.match(cmd)
    if treasure_match:
        op, expr = treasure_match.group(1), treasure_match.group(2)
        count = max(1, eval_amount(expr))
        if op == '-':
            _remove_random_equipment(character, count, '{}: {}'.format(reason, cmd))
        return

    party_gold_match = _PARTY_GOLD_CMD_RE.match(cmd)
    if party_gold_match:
        if character.leader_id != character.pk:
            return
        op, expr = party_gold_match.group(1), party_gold_match.group(2)
        amount = eval_amount(expr)
        for member in Character.objects.filter(leader=character):
            why = '{}: {}'.format(reason, cmd)
            if op == '+':
                member.add_gold(amount, why)
            elif op == '-':
                member.remove_gold(amount, why)
        return

    if _SCORPION_CMD_RE.match(cmd):
        _resolve_scorpion_swarm(character, reason)
        return

    if _GOLD_DIGGER_CURSE_RE.match(cmd):
        if character.leader_id != character.pk:
            return
        for member in Character.objects.filter(leader=character):
            if (Roll('1D6') or 1) == 1:
                _apply_stat_delta(
                    member,
                    'T',
                    -1,
                    '{}: gold digger curse'.format(reason),
                )
        return

    logger.error('Unsupported event command: %r', cmd)


def _apply_wounds_delta(character, delta, reason):
    if not delta:
        return
    CharacterParameter.objects.create(
        character=character,
        parameter=Parameter.objects.get(short_name='W'),
        value=delta,
        description=reason,
    )


def _apply_stat_delta(character, short_name, delta, reason):
    if not delta:
        return
    CharacterParameter.objects.create(
        character=character,
        parameter=Parameter.objects.get(short_name=short_name),
        value=delta,
        description=reason,
    )


def _remove_random_equipment(character, count, reason):
    from apps.game.models import Equipment
    qs = list(Equipment.objects.filter(owner=character).order_by('?')[:count])
    for equipment in qs:
        logger.error('Removing equipment %s from %s (%s)', equipment, character, reason)
        equipment.delete()


def _resolve_scorpion_swarm(character, reason):
    totals = character.get_parameter_totals()
    strength = (totals.get('strength') or {}).get('value') or 0
    kills = min(12, (Roll('1D6') or 1) + strength)
    remaining = 12 - kills
    if kills:
        character.add_gold(kills * 5, '{}: scorpion kills x5'.format(reason))
    if remaining:
        _apply_wounds_delta(character, -remaining, '{}: scorpion swarm'.format(reason))


def _apply_party_event_delta(leader, delta):
    if delta > 0:
        for _ in range(delta):
            event_roll = int('{}{}'.format(Roll('1D6'), Roll('1D6')))
            try:
                template = EventTemplate.objects.get(number=event_roll, event_type__name='Hazards')
            except EventTemplate.DoesNotExist:
                logger.error('No Hazards event for roll %s', event_roll)
                continue
            add_party_event(template, leader)
        return

    if delta < 0:
        # Cancel the newest unfinished hazard events for the whole party.
        to_cancel = list(
            Event.objects.filter(
                character=leader,
                done=False,
                template__event_type__name='Hazards',
            ).order_by('-created')[: abs(delta)]
        )
        for leader_pending in to_cancel:
            root_id = leader_pending.leader_event_id or leader_pending.pk
            Event.objects.filter(Q(pk=root_id) | Q(leader_event_id=root_id)).update(done=True)


def roll_unexpected_dungeon_event(leader):
    """Roll d66 for a Dungeon Events template and add it for the party."""
    for _ in range(36):
        event_roll = int('{}{}'.format(Roll('1D6'), Roll('1D6')))
        try:
            template = EventTemplate.objects.get(
                number=event_roll,
                event_type__name='Dungeon Events',
            )
        except EventTemplate.DoesNotExist:
            continue
        add_party_event(template, leader)
        return template

    template = EventTemplate.objects.filter(event_type__name='Dungeon Events').order_by('?').first()
    if template is None:
        logger.error('No Dungeon Events templates available')
        return None
    add_party_event(template, leader)
    return template


def warrior_event(character, event_template, tasks, leader_event=None, description_context={}, obligatory_commands=[]):
    try:
        drawn_warrior = description_context['drawn_warrior']
    except KeyError:
        raise Exception("[WE] dziwne. Nie powinno być takiej sytuacji...")

    logger.error("[WE]tasks: {}".format(tasks))
    conditional_commands = {}
    alternative_commands = {}
    character_1D6 = str(Roll('1D6'))
    party_table = bool(description_context.get('party_table'))

    # Preserve prints/commands already set from the party roll in add_party_event.
    description_context['each_warrior_print'] = description_context.get('each_warrior_print') or ''
    description_context['each_warrior_command'] = description_context.get('each_warrior_command') or ''
    description_context['drawn_warrior_print'] = description_context.get('drawn_warrior_print') or ''
    description_context['drawn_warrior_command'] = description_context.get('drawn_warrior_command') or ''
    description_context['not_drawn_warrior_print'] = description_context.get('not_drawn_warrior_print') or ''
    description_context['not_drawn_warrior_command'] = description_context.get('not_drawn_warrior_command') or ''
    description_context['party_print'] = description_context.get('party_print') or ''

    try:  # polecenia dla kazdego ale kazdy moze miec inne
        description_context['each_warrior_print'] += tasks["0"]["each_warrior_print"]
        description_context['each_warrior_command'] += tasks["0"]["each_warrior_command"]
        obligatory_commands += tasks["0"]["each_warrior_command"].split(";")
    except KeyError:
        pass
    if not party_table:
        try:  # polecenia dla każdego po losowaniu wstępnym
            description_context['each_warrior_print'] += tasks[character_1D6]["each_warrior_print"]
            description_context['each_warrior_command'] += tasks[character_1D6]["each_warrior_command"]
            obligatory_commands += tasks[character_1D6]["each_warrior_command"].split(";")
        except KeyError:
            pass

    if character == drawn_warrior:
        try:
            description_context['drawn_warrior_print'] += tasks["0"]["drawn_warrior_print"]
            description_context['drawn_warrior_command'] += tasks["0"]["drawn_warrior_command"]
            obligatory_commands += tasks["0"]["drawn_warrior_command"].split(";")
        except KeyError:
            pass
        if not party_table:
            drawn_character_1D6 = str(Roll('1D6'))
            try:
                description_context['drawn_warrior_print'] += tasks[drawn_character_1D6]["drawn_warrior_print"]
                description_context['drawn_warrior_command'] += tasks[drawn_character_1D6]["drawn_warrior_command"]
                obligatory_commands += tasks[drawn_character_1D6]["drawn_warrior_command"].split(";")
            except KeyError:
                pass
    else:
        try:
            description_context['not_drawn_warrior_print'] += tasks["0"]["not_drawn_warrior_print"]
            description_context['not_drawn_warrior_command'] += tasks["0"]["not_drawn_warrior_command"]
            obligatory_commands += tasks["0"]["not_drawn_warrior_command"].split(";")
        except KeyError:
            pass
        if not party_table:
            not_drawn_character_1D6 = str(Roll('1D6'))
            try:
                description_context['not_drawn_warrior_print'] += tasks[not_drawn_character_1D6]["not_drawn_warrior_print"]
                description_context['not_drawn_warrior_command'] += tasks[
                    not_drawn_character_1D6
                ]["not_drawn_warrior_command"]

                obligatory_commands += tasks[not_drawn_character_1D6]["not_drawn_warrior_command"].split(";")
            except KeyError:
                pass
    try:
        party_option = tasks["0"]["party_options"]  # Na to pytanie odpowiada Lider - reszta czeka
        if character != character.leader:
            party_option = "You have to wait for leader decision"
            obligatory_commands += "wait_for_leader_answer"  # to trzeba poprawić, żeby ta komenda była pierwsza
        else:
            alternative_commands['party_option'] = {}
            for party_option, command in party_option.items():
                alternative_commands['party_option'][party_option] = {
                    'description': command['description'],
                    'option_command': command['option_command'].split(";") if 'option_command' in command else []
                }
    except KeyError:
        pass
    try:
        each_warrior_options = tasks["0"]["each_warrior_options"]  # na to pytanie odpowiada każdy wojownik
        for each_warrior_option, command in each_warrior_options.items():
            alternative_commands[each_warrior_option] = {
                'choice_print': '',
                'choice_command': [],
                'description': command['description'] if 'description' in command else "",
            }

            if "choice_command" in command["0"]:
                description_context['each_warrior_choice_command'] += command["0"]["choice_command"]
                alternative_commands[each_warrior_option]['choice_command'] += command["0"]["choice_command"].split(";")

            if "choice_print" in command["0"]:
                alternative_commands[each_warrior_option]['choice_print'] += command["0"]["choice_print"]

            choice_character_1D6 = str(randint(1, 6))
            if "choice_command" in command[choice_character_1D6]:
                alternative_commands[each_warrior_option]['choice_command'] += command[
                    choice_character_1D6
                ]["choice_command"].split(";")
            if "choice_print" in command[choice_character_1D6]:
                alternative_commands[each_warrior_option]['choice_print'] += (
                    ' ' + command[choice_character_1D6]["choice_print"]
                )

    except KeyError:
        pass

    try:
        logger.error("task: {}".format(tasks["0"]["party_questions"]["0"]["choice_command"]))
        _ = tasks["0"]["party_questions"]  # Na to pytanie odpowiada Lider - reszta czeka
        if character != character.leader:
            obligatory_commands += "wait_for_leader_answer"  # to trzeba poprawić, żeby ta komenda była pierwsza
    except KeyError:
        pass
    try:
        each_warrior_questions = tasks["0"]["each_warrior_questions"]  # na to pytanie odpowiada każdy wojownik
        for each_warrior_question, command in each_warrior_questions.items():
            conditional_commands[each_warrior_question] = {
                'choice_print': '',
                'choice_command': [],
                'limit': command["limit"] if "limit" in command else "1",
                'description': command['description'] if 'description' in command else "",
            }

            if "choice_command" in command["0"]:
                description_context['each_warrior_choice_command'] += command["0"]["choice_command"]
                conditional_commands[each_warrior_question]['choice_command'] += command[
                    "0"
                ]["choice_command"].split(";")

            if "choice_print" in command["0"]:
                conditional_commands[each_warrior_question]['choice_print'] += command["0"]["choice_print"]

            choice_character_1D6 = str(randint(1, 6))
            if "choice_command" in command[choice_character_1D6]:
                conditional_commands[each_warrior_question]['choice_command'] += command[
                    choice_character_1D6
                ]["choice_command"].split(";")
            if "choice_print" in command[choice_character_1D6]:
                conditional_commands[each_warrior_question]['choice_print'] += (
                    ' ' + command[choice_character_1D6]["choice_print"]
                )

    except KeyError:
        pass

    logger.error('DESCRIPTION CONTEXT:{}'.format(description_context))

    before_form = Template("{}".format(event_template.before_form)).render(Context(description_context))
    after_form = Template("{}".format(event_template.after_form)).render(Context(description_context))
    commands = {
        'obligatory': obligatory_commands,
        'conditional': conditional_commands,
        'alternative': alternative_commands,
    }
    return Event.objects.create(
        character=character,
        template=event_template,
        before_form=before_form,
        after_form=after_form,
        command=json.dumps(commands),
        leader_event=leader_event,
    )


def add_warrior_event(event_template, character):
    party_context = {
        'drawn_warrior': character,
        'party_print': '',
        'party_command': '',
        'each_warrior_print': '',
        'each_warrior_command': '',
        'drawn_warrior_print': '',
        'drawn_warrior_command': '',
        'not_drawn_warrior_print': '',
        'not_drawn_warrior_command': '',
        'each_warrior_choice_print': '',
        'each_warrior_choice_command': '',
        'choice_question': '',

    }

    logger.error("[AWE]commands: {}".format(event_template.command))
    try:
        tasks = json.loads(event_template.command)
    except json.JSONDecodeError:
        tasks = {'error': 'JSONDecodeError'}
    warrior_event(character, event_template, tasks, None, party_context.copy())


def add_party_event(event_template, leader):
    # -----------------------------------
    drawn_warrior = Character.objects.filter(leader=leader)[
        randrange(0, Character.objects.filter(leader=leader).count())
    ]
    party_1D6 = str(Roll('1D6'))
    party_context = {
        'drawn_warrior': drawn_warrior,
        'drawn_warrior_name': drawn_warrior.name,
        'party_print': '',
        'party_command': '',
        'each_warrior_print': '',
        'each_warrior_command': '',
        'drawn_warrior_print': '',
        'drawn_warrior_command': '',
        'not_drawn_warrior_print': '',
        'not_drawn_warrior_command': '',
        'each_warrior_choice_print': '',
        'each_warrior_choice_command': '',
        'choice_question': '',

    }
    party_obligatory_commands = []
    drawn_obligatory_commands = []
    try:
        tasks = json.loads(event_template.command)
    except json.JSONDecodeError:
        tasks = {}

    zero_task = tasks.get("0") or {}
    party_table = bool(zero_task.get("party_table"))
    party_context['party_table'] = party_table

    def _merge_party_meta(task):
        if not task:
            return
        if "party_print" in task:
            party_context['party_print'] += task["party_print"]
        if "party_command" in task:
            party_context['party_command'] += task["party_command"]
            party_obligatory_commands.extend(_split_commands(task["party_command"]))

    def _merge_party_warrior_effects(task):
        if not task:
            return
        if "each_warrior_print" in task:
            party_context['each_warrior_print'] += task["each_warrior_print"]
        if "each_warrior_command" in task:
            party_context['each_warrior_command'] += task["each_warrior_command"]
            party_obligatory_commands.extend(_split_commands(task["each_warrior_command"]))
        if "drawn_warrior_print" in task:
            party_context['drawn_warrior_print'] += task["drawn_warrior_print"]
        if "drawn_warrior_command" in task:
            party_context['drawn_warrior_command'] += task["drawn_warrior_command"]
            drawn_obligatory_commands.extend(_split_commands(task["drawn_warrior_command"]))

    _merge_party_meta(zero_task)
    rolled_task = tasks.get(party_1D6) or {}
    _merge_party_meta(rolled_task)
    if party_table:
        _merge_party_warrior_effects(rolled_task)

    def _commands_for(character):
        cmds = list(party_obligatory_commands)
        if character.pk == drawn_warrior.pk:
            cmds.extend(drawn_obligatory_commands)
        return cmds

    # --- najpierw leader
    leader_event = warrior_event(
        leader, event_template, tasks, None, party_context.copy(), _commands_for(leader)
    )
    leader_event.leader_event = leader_event
    leader_event.save()
    # --- potem reszta
    for character in Character.objects.filter(leader=leader).exclude(pk=leader.pk):
        warrior_event(
            character,
            event_template,
            tasks,
            leader_event,
            party_context.copy(),
            _commands_for(character),
        )
