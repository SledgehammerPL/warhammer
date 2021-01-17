from django import forms
from people.models import Person
from .models import WarriorType, Character, Party, Journey
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field, Fieldset,HTML

class JourneyDestinationForm(forms.Form):
    destination = forms.ModelChoiceField(queryset=Journey.objects.all())
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
    leader = forms.ModelChoiceField(queryset=Character.objects.all())
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
    player = forms.ModelChoiceField(queryset=Person.objects.filter(is_superuser=False), label="Player")
    warrior_type = forms.ModelChoiceField(queryset=WarriorType.objects.all(), label="Warrior Type")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.layout.append(
            Column(
                Row(Field('name')),
                Row(Field('player')),
                Row(Field('warrior_type')),
                Submit('submit','Dodaj nową postać'),
            )
        )



class CharacterForm(forms.ModelForm):
    """Form to use with inlineformset_factory and PartyForm."""
    class Meta:
        model = Character
        fields = ['name']



