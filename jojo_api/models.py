from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=100)  # Nom du personnage
    power_description = models.TextField()   # Description des pouvoirs
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout

    def __str__(self):
        return self.name
