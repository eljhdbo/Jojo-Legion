from django.db import models

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
    image_url = models.URLField()
    part = models.ForeignKey(Part, related_name='characters', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
