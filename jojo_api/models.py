from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Part(models.Model):
    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    image_url = models.URLField()
    mal_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.title

class Character(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    image_url = models.URLField(default="https://example.com/default-image.jpg")
    part = models.ForeignKey(Part, related_name='characters', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    nb_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class CharacterLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='character_likes')
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'character')

    def __str__(self):
        return f"{self.user.username} aime {self.character.name}"
class Theory(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    content_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    image_url = models.CharField(max_length=255, null=True, blank=True)


    def get_image_url(self):
        """Retourne l'URL complète de l'image"""
        if self.image_url:
            if self.image_url.startswith('/static/'):
                return self.image_url[7:]  # Enlève '/static/' du début
            return self.image_url
        return 'images/theories/default.jpg'  # Image par défaut  # Nouveau champ

    def __str__(self):
        return self.title

class ArchivedLike(models.Model):
    ITEM_TYPE_CHOICES = [
        ('character', 'Character'),
        ('theory', 'Theory'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True)
    theory = models.ForeignKey(Theory, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = [
            ('user', 'character'),
            ('user', 'theory')
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.item_type}"