from django.urls import path
from .views import list_characters  # Assurez-vous que cette ligne importe bien la vue

urlpatterns = [
    path('characters/', list_characters, name='list-characters'),  # Assure-toi que la route est bien définie
]
