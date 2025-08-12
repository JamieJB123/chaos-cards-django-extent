from django.contrib import admin
from .models import Card

# Register card model

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_on')
    search_fields = ('title', 'content')
    list_filter = ('created_on',)
    ordering = ('-created_on',)
