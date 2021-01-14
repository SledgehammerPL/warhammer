from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Person


class PersonCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Person
        fields = ('email',)
   
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

class PersonChangeForm(UserChangeForm):

    class Meta:
        model = Person
        fields = ('email',)

