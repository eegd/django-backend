from django.contrib import admin

from app.api.models import ShoppingItem, ShoppingList


admin.site.register(ShoppingItem)
admin.site.register(ShoppingList)
