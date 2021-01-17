from django.urls import path, include
from . import views

urlpatterns = [
  # Example:
  path('',views.index, name='index'),
#  path('create_party2/',views.PartyCreateView.as_view(), name='create_party2'),
  path('choose_character/',views.choose_character, name='choose_character'),
  path('characters/',views.character_list, name='character_list'),
  path('characters/<int:character>/',views.character_profile, name='character_profile'),
  path('join_to_party/',views.join_to_party, name='join_to_party'),
  path('leave_the_party/',views.leave_the_party, name='leave_the_party'),
  path('create_party/',views.create_party, name='create_party'),
  path('choose_party_leader/',views.choose_party_leader, name='choose_party_leader'),
  path('destroy_party/',views.destroy_party, name='destroy_party'),
  path('create_character/',views.create_character, name='create_character'),
  path('trip_to/',views.trip_to, name='trip_to'),
  path('accounts/',include('django.contrib.auth.urls')),
]
