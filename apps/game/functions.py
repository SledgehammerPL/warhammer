from .models import Character, Event, EventTemplate
from random import randint, randrange
from django.db.models import Q
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

    logger.error('Unsupported event command: %r', cmd)


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


def warrior_event(character, event_template, tasks, leader_event=None, description_context={}, obligatory_commands=[]):
    try:
        drawn_warrior = description_context['drawn_warrior']
    except KeyError:
        raise Exception("[WE] dziwne. Nie powinno być takiej sytuacji...")

    logger.error("[WE]tasks: {}".format(tasks))
    conditional_commands = {}
    alternative_commands = {}
    character_1D6 = str(Roll('1D6'))
    try:  # polecenia dla kazdego ale kazdy moze miec inne - każdy dostaje tyle ile wylosuje x20 zł
        description_context['each_warrior_print'] = tasks["0"]["each_warrior_print"]
        description_context['each_warrior_command'] += tasks["0"]["each_warrior_command"]
        obligatory_commands += tasks["0"]["each_warrior_command"].split(";")
    except KeyError:
        pass
    try:  # polecenia dla każdego po losowaniu wstępnym
        description_context['each_warrior_print'] += tasks[character_1D6]["each_warrior_print"]
        description_context['each_warrior_command'] += tasks[character_1D6]["each_warrior_command"]
        obligatory_commands += tasks[character_1D6]["each_warrior_command"].split(";")
    except KeyError:
        pass

    if character == drawn_warrior:
        drawn_character_1D6 = str(Roll('1D6'))
        try:  # polecenia dla kazdego ale kazdy moze miec inne - każdy dostaje tyle ile wylosuje x20 zł
            description_context['drawn_warrior_print'] += tasks["0"]["drawn_warrior_print"]
            description_context['drawn_warrior_command'] += tasks["0"]["drawn_warrior_command"]
            obligatory_commands += tasks["0"]["drawn_warrior_command"].split(";")
        except KeyError:
            pass
        try:  # polecenia dla każdego po losowaniu wstępnym
            description_context['drawn_warrior_print'] += tasks[drawn_character_1D6]["drawn_warrior_print"]
            description_context['drawn_warrior_command'] += tasks[drawn_character_1D6]["drawn_warrior_command"]
            obligatory_commands += tasks[drawn_character_1D6]["drawn_warrior_command"].split(";")
        except KeyError:
            pass
    else:
        not_drawn_character_1D6 = str(Roll('1D6'))
        try:  # polecenia dla kazdego ale kazdy moze miec inne - każdy dostaje tyle ile wylosuje x20 zł
            description_context['not_drawn_warrior_print'] += tasks["0"]["not_drawn_warrior_print"]
            description_context['not_drawn_warrior_command'] += tasks["0"]["not_drawn_warrior_command"]
            obligatory_commands += tasks["0"]["not_drawn_warrior_command"].split(";")
        except KeyError:
            pass
        try:  # polecenia dla każdego po losowaniu wstępnym
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
    try:
        tasks = json.loads(event_template.command)
    except json.JSONDecodeError:
        tasks = {}

    zero_task = tasks.get("0") or {}
    if "party_print" in zero_task:
        party_context['party_print'] = zero_task["party_print"]
    if "party_command" in zero_task:
        party_context['party_command'] += zero_task["party_command"]
        party_obligatory_commands += _split_commands(zero_task["party_command"])

    rolled_task = tasks.get(party_1D6) or {}
    if "party_print" in rolled_task:
        party_context['party_print'] += rolled_task["party_print"]
    if "party_command" in rolled_task:
        party_context['party_command'] += rolled_task["party_command"]
        party_obligatory_commands += _split_commands(rolled_task["party_command"])
    # --- najpierw leader
    leader_event = warrior_event(leader, event_template, tasks, None, party_context.copy(), party_obligatory_commands)
    leader_event.leader_event = leader_event
    leader_event.save()
    # --- potem reszta
    for character in Character.objects.filter(leader=leader).exclude(pk=leader.pk):
        warrior_event(character, event_template, tasks, leader_event, party_context.copy(), party_obligatory_commands)
    #        messages.info(request, 'added event {} to {}'.format(event.title, character))
