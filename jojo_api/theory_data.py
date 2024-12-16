from django.contrib.auth import get_user_model
from .models import Theory

def add_initial_theories():
    User = get_user_model()
    # Récupérer ou créer un utilisateur admin
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'is_staff': True, 
            'is_superuser': True,
            'password': 'AdminMefieElijah'  # Vous devriez changer ce mot de passe
        }
    )

    theories_data = [
        {
            "title": "Kakyoin est Stone Free",
            "content": "Une théorie fascinante suggère que le Stand de Kakyoin possède une connexion cachée et mystérieuse avec Stone Free de Jolyne."
        },
        {
            "title": "Josuke s'est déplacé dans le temps pour se sauver bébé",
            "content": "Le mystérieux sauveur de Josuke bébé pourrait être une version plus âgée de Josuke lui-même."
        },
        {
            "title": "Star Platinum est Jonathan Joestar",
            "content": "Star Platinum représenterait l'esprit de Jonathan réincarné à travers Jotaro."
        },
        {
            "title": "La météorite des Flèches est faite des restes de Kars",
            "content": "Les Flèches proviendraient d'une météorite formée à partir des restes de Kars, l'ultime être vivant."
        },
        {
            "title": "Dio a planifié sa propre mort avec Pucci",
            "content": "Dio aurait orchestré sa propre mort avec l'aide de Pucci pour atteindre ses objectifs ultimes."
        },
        {
            "title": "L'Arrow Requiem a choisi Giorno intentionnellement",
            "content": "L'Arrow Requiem aurait une conscience propre, ayant choisi Giorno pour son potentiel."
        },
        {
            "title": "Le Spin de Johnny est une évolution spirituelle",
            "content": "Le Spin est une manifestation spirituelle de la résilience de Johnny Joestar."
        },
        {
            "title": "Les Stands sont hérités génétiquement",
            "content": "Les Stands seraient un trait génétique transmis dans le sang de la famille Joestar."
        },
        {
            "title": "Les Piliers étaient des précurseurs des Stands",
            "content": "Les Piliers représentaient une forme primitive des Stands."
        }
    ]

    for i, theory_data in enumerate(theories_data, 1):
        theory, created = Theory.objects.get_or_create(
            title=theory_data["title"],
            defaults={
                "content": theory_data["content"],
                "user": admin_user
            }
        )
        if created:
            print(f"Théorie {i} créée : {theory.title}")
        else:
            print(f"Théorie {i} existe déjà : {theory.title}")