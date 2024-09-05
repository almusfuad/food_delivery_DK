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
      
      
class Employee(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
      owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="employees")
      
      def __str__(self):
            return f"{self.user.username} - {self.owner.user.username}"
      