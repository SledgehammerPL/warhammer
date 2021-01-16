from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .forms import NewCharacterForm, NewPartyForm, DestroyPartyForm
from .models import WarriorLevelTemplate, Character, CharacterParameter, Parameter, Party
from random import randint

# Create your views here.

def index(request):
    context = {
    }
    return render (request,'game/index.html', context)

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
                party = form.cleaned_data['party']
                starting_wounds =  sum(randint(1,6) for i in range(template.wounds_dice))+template.wounds_modifier
                try:
                    warrior = Character.objects.create(name= form.cleaned_data['name'],player=form.cleaned_data['player'],warrior_type=warrior_type, battle_level=1,starting_wounds = starting_wounds, party = party)
                    weapon_skill = CharacterParameter.objects.create(value=template.weapon_skill,parameter=Parameter.objects.get(short_name='WS'), character = warrior, desc = 'initial value')
                    ballistic_skill = CharacterParameter.objects.create(value=template.ballistic_skill,parameter=Parameter.objects.get(short_name='BS'), character = warrior, desc = 'initial value')
                    strength = CharacterParameter.objects.create(value=template.strength,parameter=Parameter.objects.get(short_name='S'), character = warrior, desc = 'initial value')
                    toughness = CharacterParameter.objects.create(value=template.toughness,parameter=Parameter.objects.get(short_name='T'), character = warrior, desc = 'initial value')
                    wounds = CharacterParameter.objects.create(value=starting_wounds,parameter=Parameter.objects.get(short_name='W'), character = warrior, desc = 'initial value')
                    initiative = CharacterParameter.objects.create(value=template.initiative,parameter=Parameter.objects.get(short_name='I'), character = warrior, desc = 'initial value')
                    attacks = CharacterParameter.objects.create(value=template.attacks,parameter=Parameter.objects.get(short_name='A'), character = warrior, desc = 'initial value')
                    luck = CharacterParameter.objects.create(value=template.luck,parameter=Parameter.objects.get(short_name='L'), character = warrior, desc = 'initial value')
                    willpower = CharacterParameter.objects.create(value=template.willpower,parameter=Parameter.objects.get(short_name='WP'), character = warrior, desc = 'initial value')
                    pinning = CharacterParameter.objects.create(value=template.pinning,parameter=Parameter.objects.get(short_name='EP'), character = warrior, desc = 'initial value')
                    damage_dice = CharacterParameter.objects.create(value=template.damage_dice,parameter=Parameter.objects.get(short_name='DD'), character = warrior, desc = 'initial value')
                    skills = CharacterParameter.objects.create(value=template.skills,parameter=Parameter.objects.get(short_name='SK'), character = warrior, desc = 'initial value')
                    move = CharacterParameter.objects.create(value=template.move,parameter=Parameter.objects.get(short_name='M'), character = warrior, desc = 'initial value')
                    form = NewCharacterForm()
                except IndexError:
                    pass
    else:
        form = NewCharacterForm()
    context = {
        'form': form
    }
    return render (request,'game/create_character.html', context)

from django.views.generic.edit import CreateView
from .forms import PartyForm, CharacterForm
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
class PartyCreateView(CreateView):
    model = Party
    form_class = PartyForm
    success_url = reverse_lazy('success')
    template_name = 'game/team_create.html'

    def get(self, request, *args, **kwargs):
        """Overriding get method to handle inline formset."""
        # Setup the formset for Character
        CharacterFormSet = inlineformset_factory(
            parent_model=Party,
            model=Character,
            form=CharacterForm,
            can_delete=True,
            extra=1,
        )

        self.object = None
        form = self.get_form(self.get_form_class())
        member_forms = CharacterFormSet()

        return self.render_to_response(
            self.get_context_data(
                form=form,
                member_forms=member_forms,
            )
        )

    def post(self, request, *args, **kwargs):
        """Overriding post method to handle inline formsets."""
        # Setup the formset for PlanCost
        CharacterFormSet = inlineformset_factory(
            parent_model=Party,
            model=Character,
            form=CharacterForm,
            can_delete=True,
            extra=1,
        )

        self.object = None
        form = self.get_form(self.get_form_class())
        member_forms = CharacterFormSet(self.request.POST)

        if form.is_valid() and member_forms.is_valid():
            return self.form_valid(form, member_forms)

        return self.form_invalid(form, member_forms) 

def create_party(request):
    if request.method == 'POST':
        form = NewPartyForm(request.POST)
        if form.is_valid():
            try:
                party = Party.objects.create(name=form.cleaned_data['name'])
                members = form.cleaned_data['party_members']
                for party_member in members:
                   party_member.party = party
                   party_member.save()
                form = NewPartyForm()
            except ObjectDoesNotExist:
                pass
    else:
        form = NewPartyForm()
    context = {
        'form': form
    }

    return render (request,'game/create_party.html', context)
def destroy_party(request):
    if request.method == 'POST':
        form = DestroyPartyForm(request.POST)
        if form.is_valid():
            try:
                for party in form.cleaned_data['parties_to_destroy']:
                   party.delete()
                form = DestroyPartyForm()
            except ObjectDoesNotExist:
                pass
    else:
        form = DestroyPartyForm()

    context = {
        'form': form
    }

    return render (request,'game/destroy_party.html', context)

def trip_to(request):
    context = {
    }
    return render (request,'game/trip_to.html', context)
