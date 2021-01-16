from django.urls import path, include
from . import views

urlpatterns = [
  # Example:
  path('',views.index, name='index'),
  path('create_party2/',views.PartyCreateView.as_view(), name='create_party2'),
  path('create_party/',views.create_party, name='create_party'),
  path('destroy_party/',views.destroy_party, name='destroy_party'),
  path('create_character/',views.create_character, name='create_character'),
  path('trip_to/',views.trip_to, name='trip_to'),
]
