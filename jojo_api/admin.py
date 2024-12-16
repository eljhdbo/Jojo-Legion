from django.contrib import admin
from .models import User, Part, Character, CharacterLike, Theory, ArchivedLike
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('title', 'mal_id')
    search_fields = ('title',)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'part', 'nb_likes')
    search_fields = ('name',)

@admin.register(CharacterLike)
class CharacterLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'character')
    search_fields = ('user__username', 'character__name')

@admin.register(Theory)
class TheoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'content_date')
    search_fields = ('title', 'user__username')

@admin.register(ArchivedLike)
class ArchivedLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_type')  # Retiré 'liked_at' de la liste
    search_fields = ('user__username', 'item_type')