from django.urls import path
from . import views

urlpatterns = [
      path('register/', view=views.registration, name="register"),
      path('login/', view=views.user_login, name='login'),
      path('add_employee/', view=views.add_employee, name='add_employee'),
      path('logout/', view=views.user_logout, name='logout'),
]
