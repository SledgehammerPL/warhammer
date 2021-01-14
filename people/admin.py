from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import PersonCreationForm, PersonChangeForm
from .models import Person


class PersonAdmin(UserAdmin):
    add_form = PersonCreationForm
    form = PersonChangeForm
    model = Person
    list_display = ('email', 'first_name', 'last_name',)
    list_filter = ('first_name', 'last_name', )
    fieldsets = (
        (None, {'fields': ( 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email',),
        }),
    )
    ordering = ('last_name', 'first_name', )


admin.site.register(Person, PersonAdmin)
