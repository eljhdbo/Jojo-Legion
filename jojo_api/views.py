import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import F
from .models import Part, Character, User, CharacterLike, Theory, ArchivedLike
from .forms import CustomUserCreationForm
import requests
import time
def home(request):
    return render(request, 'home.html')

def list_characters(request):
    # Assurez-vous d'avoir toutes les parties
    characters = Character.objects.select_related('part').all()
    parts = Part.objects.all().order_by('title')  # Ajout d'un ordre pour une meilleure présentation
    
    if request.user.is_authenticated:
        user_likes = CharacterLike.objects.filter(user=request.user).values_list('character_id', flat=True)
        for character in characters:
            character.is_liked = character.id in user_likes
    
    # Ajoutez un print pour debug
    print(f"Nombre de parties trouvées : {parts.count()}")
    for part in parts:
        print(f"Partie : {part.title} (ID: {part.id})")
    
    return render(request, 'jojo_api/characters.html', {
        'characters': characters,
        'parts': parts
    })

@login_required
@require_http_methods(["POST"])
def like_character(request, character_id):
    try:
        character = get_object_or_404(Character, id=character_id)
        
        # Vérifier si l'utilisateur a déjà liké
        like = CharacterLike.objects.filter(user=request.user, character=character).first()
        
        if like:
            # Si le like existe, on le supprime (unlike)
            like.delete()
            Character.objects.filter(id=character_id).update(nb_likes=F('nb_likes') - 1)
            message = "Like retiré"
            liked = False
        else:
            # Si le like n'existe pas, on le crée
            CharacterLike.objects.create(
                user=request.user,
                character=character
            )
            Character.objects.filter(id=character_id).update(nb_likes=F('nb_likes') + 1)
            message = "Like ajouté"
            liked = True
            
        # Récupérer le nombre de likes mis à jour
        character.refresh_from_db()
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes': character.nb_likes,
            'message': message
        })
            
    except Exception as e:
        print(f"Erreur lors du like : {str(e)}")
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@require_http_methods(["POST"])
def like_theory(request, theory_id):
    try:
        with transaction.atomic():
            theory = get_object_or_404(Theory, id=theory_id)
            
            # Vérifier si un like existe déjà
            like = ArchivedLike.objects.filter(
                user=request.user,
                theory=theory,
                item_type='theory'
            ).first()
            
            if like:
                # Unlike
                like.delete()
                theory.likes = F('likes') - 1
                theory.save()
                theory.refresh_from_db()
                return JsonResponse({
                    'success': True,
                    'liked': False,
                    'likes': theory.likes,
                    'message': 'Like retiré'
                })
            else:
                # Like
                ArchivedLike.objects.create(
                    user=request.user,
                    theory=theory,
                    item_type='theory'
                )
                theory.likes = F('likes') + 1
                theory.save()
                theory.refresh_from_db()
                return JsonResponse({
                    'success': True,
                    'liked': True,
                    'likes': theory.likes,
                    'message': 'Like ajouté'
                })
                
    except Exception as e:
        print(f"Erreur lors du like de la théorie : {str(e)}")  # Pour le débogage
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)



def fetch_and_store_jojo_data(request):
    base_url = "https://api.jikan.moe/v4"
    
    # Mapping des parties JoJo avec leurs IDs MAL corrects
    jojo_parts = [
        {"mal_id": 14719, "title": "JoJo Part 1: Phantom Blood"},
        {"mal_id": 14719, "title": "JoJo Part 2: Battle Tendency"},
        {"mal_id": 20899, "title": "JoJo Part 3: Stardust Crusaders"},
        {"mal_id": 31933, "title": "JoJo Part 4: Diamond is Unbreakable"},
        {"mal_id": 37991, "title": "JoJo Part 5: Golden Wind"},
        {"mal_id": 48661, "title": "JoJo Part 6: Stone Ocean"}
    ]

    for part_info in jojo_parts:
        try:
            # Création de la partie
            part, created = Part.objects.get_or_create(
                mal_id=part_info["mal_id"],
                defaults={
                    "title": part_info["title"],
                    "synopsis": f"Part {part_info['title'].split(':')[0].split()[-1]}",
                    "image_url": "https://example.com/default.jpg"  # URL par défaut
                }
            )

            # Récupération des personnages avec pagination
            page = 1
            while True:
                time.sleep(1)  # Respect des limites de l'API
                characters_url = f"{base_url}/anime/{part_info['mal_id']}/characters"
                response = requests.get(characters_url, params={'page': page})
                
                if response.status_code != 200:
                    break

                data = response.json()
                characters = data.get('data', [])
                
                if not characters:
                    break

                # Création des personnages
                for char in characters:
                    if char['role'] in ['Main', 'Supporting']:
                        Character.objects.get_or_create(
                            name=char['character']['name'],
                            defaults={
                                'role': char['role'],
                                'image_url': char['character']['images']['jpg']['image_url'],
                                'part': part
                            }
                        )

                # Vérifier s'il y a une page suivante
                if not data.get('pagination', {}).get('has_next_page', False):
                    break
                    
                page += 1

        except Exception as e:
            print(f"Erreur lors du traitement de la partie {part_info['title']}: {str(e)}")
            continue

    return JsonResponse({'message': 'Données récupérées et stockées avec succès !'})

def list_theories(request):
    theories = Theory.objects.all().prefetch_related('archivedlike_set')
    
    # Pour chaque théorie, vérifions si l'utilisateur l'a déjà likée
    for theory in theories:
        # On initialise des attributs pour faciliter l'accès dans le template
        theory.is_liked = False
        if request.user.is_authenticated:
            theory.is_liked = ArchivedLike.objects.filter(
                user=request.user,
                theory=theory,
                item_type='theory'
            ).exists()
    
    return render(request, 'jojo_api/theories.html', {'theories': theories})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('home')
        else:
            messages.error(request, "Identifiants invalides. Veuillez réessayer.")

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Vous vous êtes déconnecté avec succès.")
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte a été créé avec succès. Veuillez vous connecter.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def my_likes(request):
    # Récupérer les personnages likés via CharacterLike
    liked_characters = Character.objects.filter(
        likes__user=request.user  # Utilisation de la relation inverse 'likes'
    ).select_related('part')
    
    # Récupérer les théories likées via ArchivedLike
    liked_theories = Theory.objects.filter(
        archivedlike__user=request.user,
        archivedlike__item_type='theory'
    )
    
    return render(request, 'jojo_api/my_likes.html', {
        'liked_characters': liked_characters,
        'liked_theories': liked_theories
    })
def rankings(request):
    # Récupère les 10 personnages les plus likés
    top_characters = Character.objects.select_related('part').order_by('-nb_likes')[:10]
    
    # Récupère les 10 théories les plus likées
    top_theories = Theory.objects.select_related('user').order_by('-likes')[:10]
    
    return render(request, 'jojo_api/rankings.html', {
        'top_characters': top_characters,
        'top_theories': top_theories
    })





