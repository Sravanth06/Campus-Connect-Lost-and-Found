from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'location', 'user', 'date_reported')
    list_filter = ('item_type', 'date_reported')
    search_fields = ('name', 'description', 'location')