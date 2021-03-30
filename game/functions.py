from .models import Character, Event
from random import randint, randrange
from django.template import Template, Context
from django.contrib import messages
import json
import logging
logger = logging.getLogger('error_logger')

def add_event(event_template, leader): 
    def warrior_event(character, leader_event = None):
        logger.error("{}".format(tasks))
        obligatory_commands = party_obligatory_commands[:]
        conditional_commands = {}
        alternative_commands = {}
        description_context=party_context.copy()
        character_1D6 = str(randint(1,6))
        try: # polecenia dla kazdego ale kazdy moze miec inne - każdy dostaje tyle ile wylosuje x20 zł
            description_context['each_warrior_print']=tasks["0"]["each_warrior_print"]
            description_context['each_warrior_command']+=tasks["0"]["each_warrior_command"]
            obligatory_commands +=tasks["0"]["each_warrior_command"].split(";")
        except KeyError:
            pass
        try: # polecenia dla każdego po losowaniu wstępnym
            description_context['each_warrior_print']+=tasks[character_1D6]["each_warrior_print"]
            description_context['each_warrior_command']+=tasks[character_1D6]["each_warrior_command"]
            obligatory_commands +=tasks[character_1D6]["each_warrior_command"].split(";")
        except KeyError:
            pass

        if character == drawn_warrior:
            drawn_character_1D6 = str(randint(1,6))
            try: # polecenia dla kazdego ale kazdy moze miec inne - każdy dostaje tyle ile wylosuje x20 zł
                description_context['drawn_warrior_print']+=tasks["0"]["drawn_warrior_print"]
                description_context['drawn_warrior_command']+=tasks["0"]["drawn_warrior_command"]
                obligatory_commands +=tasks["0"]["drawn_warrior_command"].split(";")
            except KeyError:
                pass
            try: # polecenia dla każdego po losowaniu wstępnym
                description_context['drawn_warrior_print']+=tasks[drawn_character_1D6]["drawn_warrior_print"]
                description_context['drawn_warrior_command']+=tasks[drawn_character_1D6]["drawn_warrior_command"]
                obligatory_commands +=tasks[drawn_character_1D6]["drawn_warrior_command"].split(";")
            except KeyError:
                pass
        else:
            not_drawn_character_1D6 = str(randint(1,6))
            try: # polecenia dla kazdego ale kazdy moze miec inne - każdy dostaje tyle ile wylosuje x20 zł
                description_context['not_drawn_warrior_print']+=tasks["0"]["not_drawn_warrior_print"]
                description_context['not_drawn_warrior_command']+=tasks["0"]["not_drawn_warrior_command"]
                obligatory_commands +=tasks["0"]["not_drawn_warrior_command"].split(";")
            except KeyError:
                pass
            try: # polecenia dla każdego po losowaniu wstępnym
                description_context['not_drawn_warrior_print']+=tasks[not_drawn_character_1D6]["not_drawn_warrior_print"]
                description_context['not_drawn_warrior_command']+=tasks[not_drawn_character_1D6]["not_drawn_warrior_command"]

                obligatory_commands +=tasks[not_drawn_character_1D6]["not_drawn_warrior_command"].split(";")
            except KeyError:
                pass
        try:
            party_option=tasks["0"]["party_options"] #Na to pytanie odpowiada Lider - reszta czeka
            if character != leader:
                party_option="You have to wait for leader decision"
                obligatory_commands +="wait_for_leader_answer" #to trzeba poprawić, żeby ta komenda była pierwsza
            else:
                alternative_commands['party_option']={}
                for party_option, command in party_option.items():
                    alternative_commands['party_option'][party_option]= {'description' : command['description'],'option_command' :command['option_command'].split(";") if 'option_command' in command else []}
        except KeyError:
            pass
        try:
            each_warrior_options=tasks["0"]["each_warrior_options"] #na to pytanie odpowiada każdy wojownik
            for each_warrior_option, command in each_warrior_options.items():
                alternative_commands[each_warrior_option]={'choice_print' :'','choice_command' :[], 'description' : command['description'] if 'description' in command else ""}

                if "choice_command" in command["0"]:
                    description_context['each_warrior_choice_command']+=command["0"]["choice_command"]
                    alternative_commands[each_warrior_option]['choice_command']+=command["0"]["choice_command"].split(";")

                if "choice_print" in command["0"]:
                    alternative_commands[each_warrior_option]['choice_print']+=command["0"]["choice_print"]

                choice_character_1D6 = str(randint(1,6))
                if "choice_command" in command[choice_character_1D6]:
                    alternative_commands[each_warrior_option]['choice_command']+=command[choice_character_1D6]["choice_command"].split(";")
                if "choice_print" in command[choice_character_1D6]:
                    alternative_commands[each_warrior_option]['choice_print']+=' '+command[choice_character_1D6]["choice_print"]

        except KeyError:
            pass

        try:
            logger.error("task: {}".format(tasks["0"]["party_questions"]["0"]["choice_command"]))
            party_question=tasks["0"]["party_questions"] #Na to pytanie odpowiada Lider - reszta czeka
            if character != leader:
                party_question="You have to wait for leader decision"
                obligatory_commands +="wait_for_leader_answer" #to trzeba poprawić, żeby ta komenda była pierwsza
        except KeyError:
            pass
        try:
            each_warrior_questions=tasks["0"]["each_warrior_questions"] #na to pytanie odpowiada każdy wojownik
            for each_warrior_question, command in each_warrior_questions.items():
                conditional_commands[each_warrior_question]={'choice_print' :'','choice_command' :[],'limit' : command["limit"] if "limit" in command else "1", 'description' : command['description'] if 'description' in command else ""}

                if "choice_command" in command["0"]:
                    description_context['each_warrior_choice_command']+=command["0"]["choice_command"]
                    conditional_commands[each_warrior_question]['choice_command']+=command["0"]["choice_command"].split(";")

                if "choice_print" in command["0"]:
                    conditional_commands[each_warrior_question]['choice_print']+=command["0"]["choice_print"]

                choice_character_1D6 = str(randint(1,6))
                if "choice_command" in command[choice_character_1D6]:
                    conditional_commands[each_warrior_question]['choice_command']+=command[choice_character_1D6]["choice_command"].split(";")
                if "choice_print" in command[choice_character_1D6]:
                    conditional_commands[each_warrior_question]['choice_print']+=' '+command[choice_character_1D6]["choice_print"]

        except KeyError:
            pass
        before_form = Template("{}".format(event_template.before_form)).render(Context(description_context))
        after_form = Template("{}".format(event_template.after_form)).render(Context(description_context))
        commands = {
                'obligatory' : obligatory_commands,
                'conditional' : conditional_commands,
                'alternative' : alternative_commands,
                }
        return Event.objects.create(character = character, event_template = event_template, before_form = before_form, after_form = after_form, command = json.dumps(commands), leader_event = leader_event)


#-----------------------------------
    drawn_warrior =  Character.objects.filter(leader=leader)[randrange(0,Character.objects.filter(leader=leader).count())]
    party_1D6 = str(randint(1,6))
    party_context = {
        'drawn_warrior' : drawn_warrior,
        'party_print' : '',
        'party_command' : '',
        'each_warrior_print' : '',
        'each_warrior_command' : '',
        'drawn_warrior_print' : '',
        'drawn_warrior_command' : '',
        'not_drawn_warrior_print' : '',
        'not_drawn_warrior_command' : '',
        'each_warrior_choice_print' : '',
        'each_warrior_choice_command' : '',
        'choice_question' : '',

    }
    party_obligatory_commands = []
    tasks = json.loads(event_template.command)
    try: # wydruk i polecenia dla wszystkich bez losowania np. kazdy traci 20szt złota
        party_context['party_print']=tasks["0"]["party_print"]
        party_context['party_command']+=tasks["0"]["party_command"]
        party_obligatory_commands += tasks["0"]["party_command"].split(";")
    except KeyError:
        pass
    try: #wydruk i polecenia po losowaniu - dla wszystkich - jesli wypadnie 1 to kazdy traci 20szt złota.
        party_context['party_print']+=tasks[party_1D6]["party_print"]
        party_context['party_command']+=tasks[party_1D6]["party_command"]
        party_obligatory_commands += tasks[party_1D6]["party_command"]
    except KeyError:
        pass
    # --- najpierw leader
    leader_event = warrior_event(leader)
    leader_event.leader_event = leader_event
    leader_event.save()
    # --- potem reszta
    for character in Character.objects.filter(leader=leader).exclude(pk=leader.pk):
        warrior_event(character, leader_event)
    #        messages.info(request, 'added event {} to {}'.format(event.title, character))


