from django.urls import path
from . import views


urlpatterns = [
      path("add_category/", view=views.add_category, name='add_category'),
      path("manage_category/", view=views.manage_category, name='manage_category')
]