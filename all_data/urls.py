from django.urls import path
from . import views

urlpatterns = [
      path('restaurants/', view=views.search_all, name='searching')
]