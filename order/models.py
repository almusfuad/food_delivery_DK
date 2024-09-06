from django.db import models
from django.contrib.auth.models import User
from item.models import Item, Modifier

# Create your models here.
class Order(models.Model):
      STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('delivered', 'Delivered'),
      ]
      
      customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
      status = models.CharField(max_length=10, choices=STATUS_CHOICES)
      total_amount = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.00)
      order_at = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
            return f"Order #{self.id} by {self.user.username} - {self.status}"
      
      
      def update_total_amount(self):
            # Calculate total amount for items
            items_total = sum(item.calculate_total_price() for item in self.order_items.all())
            
            # Calculate total amount for modifiers
            modifiers_total = sum(
                  order_modifier.modifier.price * order_modifier.quantity
                  for order_modifier in self.order_modifiers.all()
            )
            
            self.total_amount = items_total + modifiers_total
            self.save()



class OrderItem(models.Model):
      order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
      item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items')
      quantity = models.IntegerField()
      price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
      
      def __str__(self):
            return f"Order #{self.order.id} - {self.item.name} x {self.quantity} at ${self.price}"
      
      def calculate_total_price(self):
            return self.price * self.quantity
      


class OrderModifier(models.Model):
      order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_modifiers')
      modifier = models.ForeignKey(Modifier, on_delete=models.CASCADE, related_name='order_modifiers')
      quantity = models.IntegerField(default=1)
      
      def __str__(self):
            return f"{self.order.id} - {self.modifier.name}"



class Payment(models.Model):
      PAYMENT_METHOD = [
            ('card', 'Card'),
            ('cash', 'Cash')
      ]
      
      order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='payment')
      customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
      payment_method = models.CharField(max_length=5, choices=PAYMENT_METHOD)
      
      def __str__(self):
            return f"Payment for Order {self.order.id} by {self.customer.username} via {self.get_payment_method_display()}"
      
      