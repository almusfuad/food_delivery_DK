from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
      ROLE_CHOICES = [
            ('owner', 'Owner'),
            ('customer', 'Customer'),
      ]
      
      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
      role = models.CharField(max_length=10, choices=ROLE_CHOICES)
      
      def __str__(self):
            return f"{self.user.username}  - {self.get_role_display()}"     # get_role_display() helps to retrieve data from a choicefield



class Restaurant(models.Model):
      owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='restaurants')
      name = models.CharField(max_length=30)
      location = models.CharField(max_length=35)
      
      def __str__(self):
            return f"{self.name} - {self.location}" 
      
class Employee(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
      restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="employees")
      isManager = models.BooleanField(default=False, blank=True)
      
      def __str__(self):
            return f"{self.user.username} - {self.restaurant.name}"
      