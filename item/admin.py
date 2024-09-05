from django.contrib import admin
from . models import Menu, Category, Item, Modifier, ItemModifier

# Register your models here.
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Modifier)
admin.site.register(ItemModifier)