from django.urls import path, include

from . import views

urlpatterns = [
  # Example:
  path('',views.index, name='index'),
  path('choose_character/',views.choose_character, name='choose_character'),
  path('begin_adventure/',views.begin_adventure, name='begin_adventure'),
  path('end_adventure/',views.end_adventure, name='end_adventure'),
  path('make_own_party/',views.make_own_party, name='make_own_party'),
  path('choose_leader/',views.choose_leader, name='choose_leader'),
  path('characters/',views.character_list, name='character_list'),
  path('characters/<int:character>/',views.character_profile, name='character_profile'),
  path('choose_leader/',views.choose_leader, name='choose_leader'),
  path('create_character/',views.create_character, name='create_character'),
  path('trip_to/<int:target_id>/',views.trip_to, name='trip_to'),
  path('show_event/',views.show_event, name='show_event'),
  path('accounts/',include('django.contrib.auth.urls')),
  path('look_for_shop/<int:shop_id>/',views.look_for_shop, name='look_for_shop'),
  path('visit_shop/<int:shop_id>/',views.visit_shop, name='visit_shop'),
  path('prepare_to_adventure/',views.prepare_to_adventure, name='prepare_to_adventure'),
  path('wait_outside/',views.wait_outside, name='wait_outside'),
  path('visit_alehouse/',views.visit_alehouse, name='visit_alehouse'),
  path('visit_temple/',views.visit_temple, name='visit_temple'),
  path('visit_gambling_house/',views.visit_gambling_house, name='visit_gambling_house'),
  path('buy_item', views.buy_item, name='buy_item'),
  path('sell_item', views.sell_item, name='sell_item'),
]
