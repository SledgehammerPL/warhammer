from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import * 
from .models import * 
from random import randint
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Sum, F, Q,  ExpressionWrapper, BooleanField, Exists, OuterRef
from django.db.models.functions import Round
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template import Template, Context
from .functions import add_party_event, add_warrior_event, Roll
from django.views.decorators.csrf import csrf_protect

import logging
logger = logging.getLogger('error_logger')

# Create your views here.
@login_required
def index(request):
    if request.user.selected_character.active_day:
        redirect('/end_of_day/')

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
                    request.user.selected_character=warrior
                    request.user.save()
                    #request.session['character_id']=warrior.id
                    #request.session['character_name']=warrior.name
                    #request.session['leader']=True
                    #request.session['leader_name']=warrior.name
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
    you = request.user.selected_character
    event = Event.objects.filter(character=you, done =False).order_by('created').first()
   
    if event is None:
        messages.success(request, 'End of events.')
        if you.location.template.is_journey: 
            journey = you.location
            you.ticks = 1
            you.active_day = False
            if you.location.next_location:
                messages.success(request, 'Dotarłeś.')
                you.location=you.location.next_location
            else:
                messages.success(request, 'Robimy nowe settlement.')
                new_settlement = Location.objects.create(template=you.location.template.next_location.all()[0], name="settlement")
                new_settlement.name = "{} {}".format(new_settlement.template.name,new_settlement.id)
                new_settlement.save()

                journey.next_location = new_settlement
                journey.save()

                you.location=new_settlement

            you.save()
            
            if not journey.character_set.all():
                journey.delete()
             
        return redirect('/')

    try:
        commands = json.loads(event.command)
    except AttributeError:
        commands = {}

    logger.error("[SE]commands: {}".format(commands))    
    if request.method == 'POST':
        form = EventForm(request.POST,commands=commands, after_form=event.after_form)

        if form.is_valid():
            for q, v in form.data.items():
                if q.startswith('btn_'):
                    messages.success(request, commands['conditional'][v]['choice_print'])
            #Tu powinny być wykonane komendy (w stylu dodaj/odejmij gold itp)
            event.done = True
            event.save()
            you.ticks += 1
            you.save()
            return redirect('/show_event/')
    else:
        form = EventForm(commands=commands, after_form=event.after_form)

    context = {
        'event' : event,
        'form' : form,
    }
    return render (request,'game/event.html', context)



@login_required
def character_profile(request, character):
    try:
        you = Character.objects.get(pk=character, player=request.user)
        other_party_members = Character.objects.filter(leader =you.leader).exclude(id=you.id)
        equipments = Equipment.objects.filter(owner = you)
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
           'equipments' : equipments,
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
#            request.session['character_id']=form.cleaned_data['character'].id
#            request.session['character_name']=form.cleaned_data['character'].name
#            request.session['leader']=form.cleaned_data['character'] == form.cleaned_data['character'].leader
#            request.session['leader_name']=form.cleaned_data['character'].leader.name
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
        you = request.user.selected_character#Character.objects.get(pk=request.session['character_id'])
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
        you = request.user.selected_character#Character.objects.get(pk=request.session['character_id'])
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
def begin_adventure(request):
    companions = Character.objects.filter(leader=request.user.selected_character)
    adventure_template = LocationTemplate.objects.get(pk=1)
    adventure = Location.objects.create(template = adventure_template, name="caves")
    adventure.name="caves {}".format(adventure.id)
    adventure.save()

    for companion in companions:
        companion.location = adventure
        companion.save()

    return redirect('/')


@login_required
def end_adventure(request):
    companions = Character.objects.filter(leader=request.user.selected_character)
    prev_location = request.user.selected_character.location
    after_template = LocationTemplate.objects.get(pk=2)
    after = Location.objects.create(template = after_template, name="after adventure")
    after.name="after adventure {}".format(after.id)
    after.save()
    for companion in companions:
        companion.location = after
        companion.save()

    prev_location.delete()

    return redirect('/')

@login_required
def wait_outside(request):
    you = request.user.selected_character
    you.ticks = 0
    prev_location = you.location
    you.location = Location.objects.get(pk=2)
    you.save()

    if not prev_location.character_set.all():
        prev_location.delete()

    return redirect('/')


@login_required
def prepare_to_adventure(request):
    you = request.user.selected_character
    prev_location = you.location
    you.location = Location.objects.get(pk=0)
    you.ticks = 0
    you.save()

    if prev_location.id != 1 and prev_location.id !=2 and not prev_location.character_set.all():
        prev_location.delete()

    return redirect('/')


@login_required
def trip_to(request, target_id):
    if target_id in [3,4,5]:
        you = request.user.selected_character
        you.ticks = 1
        you.save()
        companions = Character.objects.filter(leader=you)
        prev_location = you.location
        journey_template = LocationTemplate.objects.get(pk=target_id)
        journey = Location.objects.create(template = journey_template, name="journey to")
        journey.name="journey {}".format(journey.id)
        journey.save()
        for companion in companions:
            companion.location = journey
            companion.save()

        prev_location.delete()
         
        channel_layer = get_channel_layer() # nie jestem pewny czy to jest potrzebne. Czy tutaj.....

        logger.error("zaczynamy! rzutow bedzie {}".format(journey.template.next_location.all()[0].no_of_dices))
        for dice_roll in range(1,2*journey.template.next_location.all()[0].no_of_dices+1):
            event_roll = "{}{}".format(Roll('1D6'),Roll('1D6'))
            logger.error("event roll: {}".format(event_roll))

            event = EventTemplate.objects.get(number=event_roll,event_type__name='Hazards')

            add_party_event(event, you.leader)

    return redirect('/show_event/')

def look_for_shop(request, shop_id):
    you = request.user.selected_character
    if you.active_day:
        return redirect('/end_of_day/')

    day = you.ticks
    
    shop = Shop.objects.get(pk=shop_id)
    if you.warrior_type in shop.forbidden.all():

        messages.success(request, 'nie dla psa kiełbasa')
        return redirect('/')

    activity, created = SettlementActivity.objects.get_or_create(character=you, location=you.location, shop=shop, defaults={'status': ShopStatus.objects.get(pk=1), 'day': day})


    if activity.status.id==0 and shop.shop_type_id != 4 and shop.shop_type_id != 5: #TB:  usun 5!
        messages.success(request, 'tu już byłeś - wypad')
        return redirect('/')
    else:
        success = Roll('{}D6'.format(you.location.template.no_of_dices))>Shop.objects.get(pk=shop_id).shop_type.availability
        you.active_day = True
        you.save()
        if success:
            if shop.shop_type_id == 3:
                activity.status=ShopStatus.objects.get(pk=1)
                activity.save()
                return redirect('/visit_alehouse/')
            if shop.shop_type_id == 4:
                activity.status=ShopStatus.objects.get(pk=0)
                activity.save()
                return redirect('/visit_gambling_house/')
            if shop.shop_type_id == 5:
                activity.status=ShopStatus.objects.get(pk=0)
                activity.save()
                return redirect('/visit_temple/')
            if shop.shop_type_id == 6:
                activity.status=ShopStatus.objects.get(pk=0)
                activity.save()
                return redirect('/visit_alchemists_laboratory/')
            else:
                activity.status=ShopStatus.objects.get(pk=0)
                activity.save()
                return redirect('/visit_shop/{}/'.format(shop_id))
        else:
            activity.status=ShopStatus.objects.get(pk=-1)
            activity.save()
            context = {
                    'text' : 'Cały dzień stracony i nic...',
            }
            return render (request,'game/modal.html', context)

def visit_shop(request, shop_id):
    from django.db.models.expressions import Func
    from django.db.models.functions.mixins import (
        FixDecimalInputMixin, NumericOutputFieldMixin,
    )
    class Random(NumericOutputFieldMixin, Func):
       function = 'RANDOM'
       arity = 0

       def as_mysql(self, compiler, connection, **extra_context):
           return super().as_sql(compiler, connection, function='RAND', **extra_context)

       def as_oracle(self, compiler, connection, **extra_context):
           return super().as_sql(compiler, connection, function='DBMS_RANDOM.VALUE', **extra_context)

       def as_sqlite(self, compiler, connection, **extra_context):
           return super().as_sql(compiler, connection, function='RAND', **extra_context)

       def get_group_by_cols(self, alias=None):
           return []

    shop = Shop.objects.get(pk=shop_id)

    you = request.user.selected_character
    my_equipments = Equipment.objects.filter(item=OuterRef('pk'), owner=you)
    possible_items = Item.objects.filter(available_in=shop).annotate(dice_roll=sum(Round(Random()*5)+1 for i in range(request.user.selected_character.location.template.no_of_dices))).annotate(available = ExpressionWrapper(Q(dice_roll__gte=F('chance_to_be_in_shop')),output_field=BooleanField())).annotate(to_sell=Exists(my_equipments))
    context = {
        'shop' : shop,
        'possible_items' : possible_items,
        'user' : request.user,
    }
    return render (request,'game/visit_shop.html', context)

def visit_temple(request):
    you = request.user.selected_character
    if request.method == 'POST':
        if 'Exit' not in request.POST:
            form = TempleForm(request.POST, gold=you.get_current_gold())
            you.remove_gold(50,'Sacrifice in Temple')
            if form.is_valid():
                roll = Roll('1D6')
                # TB: TRZEBA DODAC SKILLE!!!!
                if roll == 3:
                    text = "During any one turn in the next adventure, your Warrior's Attacks are doubled."
                elif roll == 4:
                    text = "Your Warrior's hand is guided by powers unseen. For any one Attack in the next adventure, he may add +3 to his to hit roll"
                elif roll == 5:
                    text = "Your Warrior may ignore the damage caused by any one Attack made against him in the next adventure, when the blow is mysticaly deflected at the last moment."
                elif roll == 6:
                    text = "Your Warrior may roll an extra 1D6 dice when rolling the damage for any one Attack in the next adventure."
                else:
                    text = "The gods are not listening, and your Warrior's pleas go unanswered"
                context = {
                    'text' : text,
                }

                return render (request,'game/modal.html', context)
        else:
            return redirect ('/end_of_day/')
    else:
         form = TempleForm(gold=you.get_current_gold())


    context = {
        'text' : "Between adventures, many Warriors come to the local temple to offer up prayers and sacrifice in thanks for the adventure just completed, and for aid in the next.",
        'form' : form,
    }
    return render (request,'game/simple_modal_form.html', context)

def visit_alchemists_laboratory(request):
    you = request.user.selected_character
    if request.method == 'POST':
        form = AlchemistsForm(request.POST, character=request.user.selected_character)
        if form.is_valid():
            no_of_dices = form.cleaned_data['dices']
            item = form.cleaned_data['item']
            roll_sum = 0
            for dice in range(1, no_of_dices+1):
               roll = Roll('1D6')
               if roll == 1:
                   roll_sum = 0
                   break
               else:
                  roll_sum += roll
            if roll_sum == 0:
                text = "The transmutation fails and the item fizzies away until nothing is left but a pile of sludge."
            else:
                text = "The transmutation succeeds. You earn {} gold.".format(roll_sum*25)
                you.add_gold(roll_sum*25,'Transmutation of {} into gold'.format(item.item.name))
            item.delete()
            context = {
                'text' : text,
            }

            return render (request,'game/modal.html', context)

    else:
        form = AlchemistsForm(character = request.user.selected_character)


    context = {
        'form' : form,
    }
    return render (request,'game/simple_form.html', context)


def visit_gambling_house(request):
    if request.method == 'POST':
        form = GamblingForm(request.POST)
        if form.is_valid():
            event_roll = Roll('1D6')
            bet = form.cleaned_data['bet'] * Roll('1D6')
            you = request.user.selected_character
            most_valuable_item = Equipment.objects.filter(owner=you).order_by('-item__sell_price')[0]
            if event_roll == 1:
                result, item = you.remove_gold_and_most_valuable_item_if_not_enough(bet,'Lost in Gambling House')

                text = 'Your Warrior is stiched-up with minutes, the sharp-eyed owners taking him for all he has. Your Warrior loses {}.'.format(" all gold and {}".format(item) if item else "{} gold.".format(bet))
            elif event_roll == 6:
                text = "Luck is with you Warrior today, and he quickly wins {} gold.".format(bet)
                you.add_gold(bet,'Win in Gambling House')

            else:
                text = "After a pleasurable day, he finishes evens. Still, nothing lost, nothing gained"
            context = {
                    'text' : text,
            }
            return render (request,'game/modal.html', context)
    else:
        form = GamblingForm()

    context = {
        'form' : form,
    }
    return render (request,'game/simple_form.html', context)

def visit_alehouse(request):
    you = request.user.selected_character
    event_roll=Roll(you.warrior_type.alehouse_roll)
    
    event = EventTemplate.objects.get(number=event_roll,event_type__name='Alehouse')
    add_warrior_event(event, you)
    return redirect('/end_of_day/')

def end_of_day(request):
    payer = request.user.selected_character
    if payer.pay_living_expenses():
        payer.active_day = False
        payer.save()
        event_roll = "{}{}".format(Roll('1D6'),Roll('1D6'))
        event_roll = "25"
        event = EventTemplate.objects.get(number=event_roll,event_type__name='Settlement Events')
        add_warrior_event(event, payer)
        return redirect('/show_event/')
    else:
        return redirect('/wait_outside/')


####################################################

@csrf_protect
def buy_item(request):
    code = request.POST.get("item")
    price = int(request.POST.get("price"))
    seller = request.POST.get("seller")
    buyer = request.user.selected_character
    if buyer.buy_item(code, price, seller):
        result = "ok"
    else:
        result = "no way";
    return JsonResponse({
        'result' : result,
        'gold' : buyer.get_current_gold(),
        'price' : price,
        'item' : Item.objects.get(code=code).name,
    })
@csrf_protect
def sell_item(request):
    code = request.POST.get("item")
    price = int(request.POST.get("price"))
    buyer = request.POST.get("buyer")
    seller = request.user.selected_character
    result = seller.sell_item(code, price, buyer)
    return JsonResponse({
        'result' : result,
        'gold' : seller.get_current_gold(),
        'price' : price,
        'item' : Item.objects.get(code=code).name,
    })

