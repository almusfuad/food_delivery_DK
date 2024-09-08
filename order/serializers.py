from rest_framework import serializers
from .models import Order, OrderItem, OrderModifier, Payment


class OrderItemSerializer(serializers.ModelSerializer):
      class Meta:
            model = OrderItem
            fields = ['item', 'quantity', 'price']
            

class OrderModifierSerializer(serializers.ModelSerializer):
      class Meta:
            model = OrderModifier
            fields = ['modifier', 'quantity']
            

class PaymentSerializer(serializers.ModelSerializer):
      class Meta:
            model = Payment
            fields = ['payment_method']

            
class OrderSerializer(serializers.ModelSerializer):
      order_items = OrderItemSerializer(many = True)
      order_modifiers = OrderModifierSerializer(many = True, required = False)
      payment = PaymentSerializer()
      
      class Meta:
            model = Order
            fields = ['customer', 'restaurant', 'status', 'total_amount', 'order_items', 'order_modifiers', 'payment']
            read_only_fields = ['total_amount']
            
      def create(self, validated_data):
            # Extract nested data
            order_items_data = validated_data.pop('order_items')
            order_modifiers_data = validated_data.pop('order_modifiers', [])  # Default empty modifiers
            payment_data = validated_data.pop('payment')
            
            # create order
            order = Order.objects.create(**validated_data)
            
            # create related order items
            for item_data in order_items_data:
                  OrderItem.objects.create(order=order, **item_data)
                  
            # create related order modifiers
            for modifier_data in order_modifiers_data:
                  OrderModifier.objects.create(order=order, **modifier_data)
                  
            # create payment
            Payment.objects.create(order=order, customer=order.customer, **payment_data)
            
            # update total amount for order
            order.update_total_amount()
            
            return order