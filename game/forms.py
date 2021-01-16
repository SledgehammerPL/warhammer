from django import forms
from people.models import Person
from .models import WarriorType, Character, Party
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field, Fieldset,HTML


class NewCharacterForm(forms.Form):
    name = forms.CharField(label = "Name", max_length=100, widget=forms.TextInput(), required = True)
    player = forms.ModelChoiceField(queryset=Person.objects.filter(is_superuser=False), label="Player")
    warrior_type = forms.ModelChoiceField(queryset=WarriorType.objects.all(), label="Warrior Type")
    party = forms.ModelChoiceField(queryset=Party.objects.all(), label="Party")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.layout.append(
            Column(
                Row(Field('name')),
                Row(Field('player')),
                Row(Field('warrior_type')),
                Row(Field('party')),
                Submit('submit','Dodaj nową postać'),
            )
        )


class NewPartyForm(forms.Form):
    name = forms.CharField(label = "Name", max_length=100, widget=forms.TextInput(), required = True)
    party_members = forms.ModelMultipleChoiceField(queryset=Character.objects.filter(party__isnull=True))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.layout.append(
            Column(
                Row(Field('name')),
                Row(Field('party_members')),
                Submit('submit','Utwórz nową drużynę'),
            )
        )
class DestroyPartyForm(forms.Form):
    parties_to_destroy = forms.ModelMultipleChoiceField(queryset=Party.objects.all())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.layout.append(
            Column(
                Row(Field('parties_to_destroy')),
                Submit('submit','Rozwiąż drużyny'),
            )
        )


class PartyForm(forms.ModelForm):
    """Model Form for Party model."""
    class Meta:
        model = Party
        fields = ['name']


class CharacterForm(forms.ModelForm):
    """Form to use with inlineformset_factory and PartyForm."""
    class Meta:
        model = Character
        fields = ['name']



