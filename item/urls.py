from django.urls import path
from . import views


urlpatterns = [
      path("add_category/", view=views.add_category, name='add_category'),
      path("add_menu/", view=views.add_menu, name='add_menu'),
      path("add_item/", view=views.add_item, name='add_item'),
      path("add_modifier/", view=views.add_modifier, name='add_modifier'),
]