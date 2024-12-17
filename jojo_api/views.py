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

def home(request):
    return render(request, 'home.html')

def list_characters(request):
    characters = Character.objects.select_related('part').all()
    
    # Si l'utilisateur est connecté, on récupère ses likes
    if request.user.is_authenticated:
        user_likes = CharacterLike.objects.filter(user=request.user).values_list('character_id', flat=True)
        for character in characters:
            character.is_liked = character.id in user_likes
    
    parts = Part.objects.all()
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
    try:
        anime_response = requests.get(f"{base_url}/anime?q=JoJo")
        anime_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Erreur lors de la récupération des données : {e}'}, status=500)

    anime_data = anime_response.json().get('data', [])
    valid_titles = [
        "JoJo no Kimyou na Bouken Part 1: Phantom Blood",
        "JoJo no Kimyou na Bouken Part 2: Sentou Chouryuu",
        "JoJo no Kimyou na Bouken Part 3: Stardust Crusaders",
        "JoJo no Kimyou na Bouken Part 4: Diamond wa Kudakenai",
        "JoJo no Kimyou na Bouken Part 5: Ougon no Kaze",
        "JoJo no Kimyou na Bouken Part 6: Stone Ocean",
    ]

    for anime in anime_data:
        if anime['title'] in valid_titles:
            part, _ = Part.objects.get_or_create(
                mal_id=anime['mal_id'],
                defaults={
                    'title': anime['title'],
                    'synopsis': anime.get('synopsis', 'Aucune description disponible'),
                    'image_url': anime['images']['jpg']['image_url'],
                }
            )
            
            try:
                characters_response = requests.get(f"{base_url}/anime/{anime['mal_id']}/characters")
                if characters_response.status_code == 200:
                    char_data = characters_response.json().get('data', [])
                    for char in char_data:
                        Character.objects.get_or_create(
                            name=char['character']['name'],
                            defaults={
                                'role': char.get('role', 'Inconnu'),
                                'image_url': char['character']['images']['jpg']['image_url'],
                                'part': part,
                            }
                        )
            except requests.exceptions.RequestException:
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