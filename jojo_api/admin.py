from django.contrib import admin
from .models import Part, Character

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('title', 'mal_id')  # Affiche ces colonnes dans l'admin

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'part')  # Affiche ces colonnes dans l'admin
