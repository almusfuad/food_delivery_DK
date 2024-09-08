from django.urls import path
from . import views

urlpatterns = [
      path('restaurant/', view=views.restaurant_data, name='all_restaurant')
]