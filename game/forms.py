from django import forms
from people.models import Person
from .models import WarriorType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field, Fieldset,HTML


class NewCharacterForm(forms.Form):
    name = forms.CharField(label = "Name", max_length=100, widget=forms.TextInput(), required = True)
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




