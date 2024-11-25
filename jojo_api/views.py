import requests
from django.http import JsonResponse
from .models import Part, Character
from django.shortcuts import render  # Assurez-vous que cette ligne est présente
from .models import Character  # Importez aussi vos modèles


def fetch_and_store_jojo_data(request):
    base_url = "https://api.jikan.moe/v4"

    anime_response = requests.get(f"{base_url}/anime?q=JoJo")
    if anime_response.status_code != 200:
        return JsonResponse({'error': 'Impossible de récupérer les parties'}, status=anime_response.status_code)

    anime_data = anime_response.json()['data']

    # Liste des titres spécifiques à JoJo's Bizarre Adventure
    valid_titles = [
        "JoJo no Kimyou na Bouken",
        "JoJo no Kimyou na Bouken Part 3: Stardust Crusaders",
        "JoJo no Kimyou na Bouken Part 4: Diamond wa Kudakenai",
        "JoJo no Kimyou na Bouken Part 5: Ougon no Kaze",
        "JoJo no Kimyou na Bouken Part 6: Stone Ocean",
        "JoJo no Kimyou na Bouken: Phantom Blood",
    ]

    for anime in anime_data:
        # Vérifie si le titre contient "JoJo" et figure dans la liste des titres valides
        if any(title in anime['title'] for title in valid_titles):
            part, created = Part.objects.get_or_create(
                mal_id=anime['mal_id'],
                defaults={
                    'title': anime['title'],
                    'synopsis': anime.get('synopsis', 'Aucune description disponible'),
                    'image_url': anime['images']['jpg']['image_url'],
                }
            )

            # Récupérer les personnages associés
            characters_response = requests.get(f"{base_url}/anime/{anime['mal_id']}/characters")
            if characters_response.status_code == 200:
                char_data = characters_response.json()['data']
                for char in char_data:
                    Character.objects.get_or_create(
                        name=char['character']['name'],
                        part=part,
                        defaults={
                            'role': char.get('role', 'Inconnu'),
                            'image_url': char['character']['images']['jpg']['image_url'],
                        }
                    )

    return JsonResponse({'message': 'Données récupérées et stockées avec succès !'})


def list_characters(request):
    characters = Character.objects.all()  # Récupère tous les personnages de la base
    return render(request, 'jojo_api/characters.html', {'characters': characters})
