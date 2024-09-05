from django.urls import path
from . import views

urlpatterns = [
      path('register/', view=views.registration, name="register"),
      path('login/', view=views.user_login, name='login'),
      path('logout/', view=views.user_logout, name='logout'),
      path('owner_employee/', view=views.owner_manage_employee, name="owner_employee"),
]
