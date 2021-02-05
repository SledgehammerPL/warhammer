from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import * 
from .models import * 
from random import randint
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template import Template, Context
from .functions import add_event

import logging
logger = logging.getLogger('error_logger')

# Create your views here.
@login_required
def index(request):
    context = {
    }
    return render (request,'game/index.html', context)

@login_required
def create_character(request):
    if request.method == 'POST':
        form = NewCharacterForm(request.POST)
        if form.is_valid():
            try:
                warrior = Character.objects.get(name=form.cleaned_data['name'])
#                form.invalid()
            except ObjectDoesNotExist:
                warrior_type = form.cleaned_data['warrior_type']
                template = WarriorLevelTemplate.objects.filter(level=1,warrior_type=warrior_type)[0]
                starting_wounds =  sum(randint(1,6) for i in range(template.wounds_dice))+template.wounds_modifier
                try:
                    warrior = Character.objects.create(name= form.cleaned_data['name'],player=request.user,warrior_type=warrior_type, battle_level=1,starting_wounds = starting_wounds)
                    warrior.leader = warrior
                    warrior.save()
                    weapon_skill = CharacterParameter.objects.create(value=template.weapon_skill,parameter=Parameter.objects.get(short_name='WS'), character = warrior, description = 'initial value of weapon skill')
                    ballistic_skill = CharacterParameter.objects.create(value=template.ballistic_skill,parameter=Parameter.objects.get(short_name='BS'), character = warrior, description = 'initial value of ballistic skill')
                    strength = CharacterParameter.objects.create(value=template.strength,parameter=Parameter.objects.get(short_name='S'), character = warrior, description = 'initial value of strength')
                    toughness = CharacterParameter.objects.create(value=template.toughness,parameter=Parameter.objects.get(short_name='T'), character = warrior, description = 'initial value of toughness')
                    wounds = CharacterParameter.objects.create(value=starting_wounds,parameter=Parameter.objects.get(short_name='W'), character = warrior, description = 'initial value of wounds')
                    initiative = CharacterParameter.objects.create(value=template.initiative,parameter=Parameter.objects.get(short_name='I'), character = warrior, description = 'initial value of initiative')
                    attacks = CharacterParameter.objects.create(value=template.attacks,parameter=Parameter.objects.get(short_name='A'), character = warrior, description = 'initial value of attacks')
                    luck = CharacterParameter.objects.create(value=template.luck,parameter=Parameter.objects.get(short_name='L'), character = warrior, description = 'initial value of luck')
                    willpower = CharacterParameter.objects.create(value=template.willpower,parameter=Parameter.objects.get(short_name='WP'), character = warrior, description = 'initial value of willpower')
                    pinning = CharacterParameter.objects.create(value=template.pinning,parameter=Parameter.objects.get(short_name='EP'), character = warrior, description = 'initial value of escape pinning')
                    damage_dice = CharacterParameter.objects.create(value=template.damage_dice,parameter=Parameter.objects.get(short_name='DD'), character = warrior, description = 'initial value of damage dice')
                    skills = CharacterParameter.objects.create(value=template.skills,parameter=Parameter.objects.get(short_name='SK'), character = warrior, description = 'initial value of skills')
                    move = CharacterParameter.objects.create(value=template.move,parameter=Parameter.objects.get(short_name='M'), character = warrior, description = 'initial value of move')
                    request.session['character_id']=warrior.id
                    request.session['character_name']=warrior.name
                    request.session['leader']=True
                    request.session['leader_name']=warrior.name
                    form = NewCharacterForm()
                    messages.success(request, 'New Character created.')
                except IndexError:
                    pass
    else:
        form = NewCharacterForm()
    context = {
        'form': form
    }
    return render (request,'game/create_character.html', context)

@login_required
def character_list(request):
    characters = Character.objects.filter(player=request.user)
    context = {
        'characters' : characters,
    }
    return render (request,'game/character_list.html', context)

@login_required
def show_event(request):
    try:
        you = Character.objects.get(pk=request.session['character_id'])
        event = Event.objects.filter(character=you, done =False).order_by('created').first()
        if event is None:
            messages.success(request, 'End of events.')
            return redirect('/')
        if request.method == 'POST':
            form = EventForm(request.POST)

            if form.is_valid():
                event.done = True
                event.save()
                return redirect('/show_event/')
        else:
            form = EventForm()

        context = {
            'event' : event,
            'form' : form,
        }
        return render (request,'game/event.html', context)
    except ObjectDoesNotExist:
        return redirect('/characters/')



@login_required
def character_profile(request, character):
    try:
        you = Character.objects.get(pk=character, player=request.user)
        other_party_members = Character.objects.filter(leader =you.leader).exclude(id=you.id)

        parameters = {
                'wounds' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'W').aggregate(value=Sum('value')),
                'move' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'M').aggregate(value=Sum('value')),
                'weapon_skill' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'WS').aggregate(value=Sum('value')),
                'ballistic_skill' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'BS').aggregate(value=Sum('value')),
                'strength' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'S').aggregate(value=Sum('value')),
                'toughness' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'T').aggregate(value=Sum('value')),
                'initiative' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'I').aggregate(value=Sum('value')),
                'attacks' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'A').aggregate(value=Sum('value')),
                'luck' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'L').aggregate(value=Sum('value')),
                'willpower' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'WP').aggregate(value=Sum('value')),
                'pinning' :  CharacterParameter.objects.filter(character=you, parameter__short_name = 'EP').aggregate(value=Sum('value')),
                }
        context = {
           'character' : you,
           'parameters' : parameters,
           'other_party_members' : other_party_members,
        }
        return render (request,'game/character_profile.html', context)
    except ObjectDoesNotExist:
        return redirect('/characters/')

@login_required
def choose_character(request):
    if request.method == 'POST':
        try:
            form = ChooseCharacterForm(request.POST, user=request.user, initial = {'character':request.session['character']})
        except KeyError:
             form = ChooseCharacterForm(request.POST, user=request.user)

        if form.is_valid():
            user = request.user
            user.selected_character=form.cleaned_data['character']
            user.save()
            request.session['character_id']=form.cleaned_data['character'].id
            request.session['character_name']=form.cleaned_data['character'].name
            request.session['leader']=form.cleaned_data['character'] == form.cleaned_data['character'].leader
            request.session['leader_name']=form.cleaned_data['character'].leader.name
            messages.success(request, 'Character successfully choosen.')
            return redirect('/')

    else:
        form = ChooseCharacterForm(user=request.user)

    context = {
        'form' : form,
    }
    return render (request,'game/simple_form.html', context)


@login_required
def choose_leader(request):
    try: 
        you = Character.objects.get(pk=request.session['character_id'])
        if request.method == 'POST':
            form = PartyLeaderForm(request.POST)

            if form.is_valid():
                you.leader = form.cleaned_data['leader']
                you.save()
                request.session['leader']=you == you.leader
                request.session['leader_name']= you.leader.name
                messages.success(request, 'Leader successfully choosen.')
                return redirect('/')
        else:
            form = PartyLeaderForm()

        context = {
            'form' : form,
        }
        return render (request,'game/simple_form.html', context)
    except ObjectDoesNotExist:
         return redirect('/')

@login_required
def make_own_party(request):
    try: 
        you = Character.objects.get(pk=request.session['character_id'])
        if request.method == 'POST':
            form = YesNoForm(request.POST, question="Are you sure you want to leave the {}'s party?".format(you.leader))

            if form.is_valid():
                if form.cleaned_data['answer']=='True':
                    for character in  Character.objects.filter(leader=you.leader):
                        character.leader=character
                        character.save()
                        request.session['leader']=True
                        request.session['leader_name']=character.name
                    messages.success(request, 'You are the leader of own party')

                return redirect('/')
        else:
            form = YesNoForm(question="Are you sure you want to leave the  {}'s party?".format(you.leader))

        context = {
            'form' : form,
        }
        return render (request,'game/simple_form.html', context)
    except ObjectDoesNotExist:
         return redirect('/')

@login_required
def trip_to(request):
    if request.method == 'POST':
        form = JourneyDestinationForm(request.POST)
        if form.is_valid():
            you = Character.objects.get(pk=request.session['character_id'])
            channel_layer = get_channel_layer()
            trip_to = form.cleaned_data['destination']
            for roll in range(1,trip_to.rolls +1):
                event_roll = "{}{}".format(randint(1,6),randint(1,6))
                event_roll = "13" #TB: Devel line
                event = EventTemplate.objects.get(number=event_roll,event_type__name='Hazards')

                add_event(event, you.leader)

    else:
        form = JourneyDestinationForm()
    context = {
        'form' : form,
    }
    return render (request,'game/simple_form.html', context)

