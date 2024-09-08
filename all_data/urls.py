from django.urls import path
from . import views

urlpatterns = [
      path('restaurants/', view=views.search_all, name='searching'),
      path('owner_restaurants/', view=views.owner_restaurants, name='owner_restaurant'),
      path('manager_employees/', view=views.manager_employees, name='manager_employees')
]