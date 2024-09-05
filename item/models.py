from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
      name = models.CharField(max_length=50)
      description = models.TextField(blank=True)
      
      def __str__(self):
            return f"{self.user.username}-{self.name}"
      
class Menu(models.Model):
      category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="menus")
      name = models.CharField(max_length=50)
      description = models.TextField(blank=True)
      
      def __str__(self):
            return f"{self.category.name} - {self.name}"
      

class Item(models.Model):
      menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
      name = models.CharField(max_length=40)
      description = models.TextField(blank=True)
      price = models.DecimalField(max_digits=6, decimal_places=2)
      
      def __str__(self):
            return f"{self.menu.name} - {self.name}"


class Modifier(models.Model):
      name = models.CharField(max_length=60)
      description = models.TextField(blank=True)
      price = models.DecimalField(max_digits=4, decimal_places=1)
      update_at = models.DateTimeField(auto_now=True)
      
      
      def __str__(self):
            return f"{self.name}"
      
class ItemModifier(models.Model):
      item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="modifiers")
      modifier = models.ForeignKey(Modifier, on_delete=models.CASCADE, related_name="items")
      
      def __str__(self):
            return f"{self.item.name} - {self.modifier.name}"
      