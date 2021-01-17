from django.urls import path, include
from . import views

urlpatterns = [
  # Example:
  path('',views.index, name='index'),
#  path('create_party2/',views.PartyCreateView.as_view(), name='create_party2'),
  path('choose_character/',views.choose_character, name='choose_character'),
  path('make_own_party/',views.make_own_party, name='make_own_party'),
  path('choose_leader/',views.choose_leader, name='choose_leader'),
  path('characters/',views.character_list, name='character_list'),
  path('characters/<int:character>/',views.character_profile, name='character_profile'),
  path('choose_leader/',views.choose_leader, name='choose_leader'),
  path('create_character/',views.create_character, name='create_character'),
  path('trip_to/',views.trip_to, name='trip_to'),
  path('accounts/',include('django.contrib.auth.urls')),
]
