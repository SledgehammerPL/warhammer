from django import forms
from people.models import Person
from .models import WarriorType, Character, JourneyTable
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field, Fieldset,HTML,Button, ButtonHolder
from django.db.models import F
from django.utils.text import slugify
import json
import logging
logger = logging.getLogger('error_logger')


class JourneyDestinationForm(forms.Form):
    destination = forms.ModelChoiceField(queryset=JourneyTable.objects.all())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.layout.append(
            Column(
                Row(Field('destination')),
                Submit('submit','Wybierz cel'),
            )
        )

class EventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        try:
            commands = kwargs.pop('commands')
            after_form = kwargs.pop('after_form')
        except KeyError:
            commands = {}
            after_form =""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        choices =[]
        if "alternative" in commands:
            if 'party_option' in commands['alternative']:
                for option, option_spec in commands['alternative']['party_option'].items():
                    logger.error("{}:{}".format(option, option_spec))
                    choices.append(tuple((option,option_spec["description"])))
                logger.error("{}".format(choices))
                self.fields["option"] = forms.ChoiceField(label="",choices=choices,widget=forms.RadioSelect)
                self.helper.layout.append('option')
        for question, question_spec in commands['conditional'].items():
            if "limit" in question_spec:
                for i in range(int(question_spec["limit"])):
                    self.fields["choice_{}_{}".format(question.lower().replace(' ','_'),i)] = forms.BooleanField(label=question_spec["description"], required=False)
                    self.helper.layout.append('choice_{}_{}'.format(question.lower().replace(' ','_'),i))
#            self.helper.layout.append(Submit("btn_"+question,question))
        self.helper.layout.append(HTML("<p>{}</p>".format(after_form)))
        self.helper.layout.append(Submit('submit','Next Event'))
        self.helper.all().wrap_together(Column)


class YesNoForm(forms.Form):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    answer = forms.ChoiceField(choices=BOOL_CHOICES, initial = False)
    question = ""
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].label = question
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.layout.append(
            Column(
                Row(Field('answer')),
                Submit('submit','Zatwierdź wybór'),
            )
        )

class ChooseCharacterForm(forms.Form):
    character = forms.ModelChoiceField(queryset=None)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['character'].queryset = Character.objects.filter(player=user)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.layout.append(
            Column(
                Row(Field('character')),
                Submit('submit','Wybierz postać'),
            )
        )



class PartyLeaderForm(forms.Form):
    leader = forms.ModelChoiceField(queryset=Character.objects.filter(leader=F('pk')))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.layout.append(
            Column(
                Row(Field('leader')),
                Submit('submit','Wybierz lidera'),
            )
        )



class NewCharacterForm(forms.Form):
    name = forms.CharField(label = "Name", max_length=100, widget=forms.TextInput())
    warrior_type = forms.ModelChoiceField(queryset=WarriorType.objects.all(), label="Warrior Type")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.layout.append(
            Column(
                Row(Field('name')),
                Row(Field('warrior_type')),
                Submit('submit','Dodaj nową postać'),
            )
        )



class CharacterForm(forms.ModelForm):
    """Form to use with inlineformset_factory and PartyForm."""
    class Meta:
        model = Character
        fields = ['name']



