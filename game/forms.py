from django import forms
from people.models import Person
from .models import WarriorType, Character, JourneyTable
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field, Fieldset,HTML
from django.db.models import F
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
    commands = {}
    def __init__(self, *args, **kwargs):
        try:
            self.commands = kwargs.pop('commands')
            logger.error("EventForm.commands: {}".format(self.commands))
        except KeyError:
            pass
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.layout.append(
            Column(
                Submit('submit','Next Event'),
            )
        )


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



