from django import forms


class NewCharacterForm(forms.Form):
    name = forms.CharField(label = "Name", maxlength=100, widget=forms.TextInput(), required = True)
    player = forms.ModelChoiceField(queryset=Peron.objects.filter(is_superuser=False), label="Player")
    warrior_type_id = forms.ModelChoiceField(queryset=WarriorType.objects.all, label="Warrior Type")


