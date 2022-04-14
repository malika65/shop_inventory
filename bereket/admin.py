from django.contrib import admin

from .models import Product, Client, Sale, Transaction, Cash, Consumption

admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Sale)
admin.site.register(Transaction)
admin.site.register(Cash)
admin.site.register(Consumption)