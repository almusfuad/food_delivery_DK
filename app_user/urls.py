from django.urls import path
from . import views

urlpatterns = [
      path('register/', view=views.registration, name="register"),
      path('login/', view=views.user_login, name='login'),
      path('logout/', view=views.user_logout, name='logout'),
      path('add_employee/', view=views.add_employee, name="add_employee"),
      path('add_restaurant/', view=views.manage_restaurant, name='add_restaurant'),
]
