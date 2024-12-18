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
           'password': 'AdminMefieElijah'
       }
   )

   theories_data = [
   {
        "title": "Kakyoin est Stone Free",
        "content": "Une théorie fascinante et intrigante explore la possibilité que le Stand de Kakyoin, Hierophant Green, partage des similarités ou des connexions cachées avec Stone Free de Jolyne. Cela pourrait suggérer un lien symbolique ou thématique entre les deux personnages, renforçant l'idée que les Stands évoluent ou se réincarnent sous de nouvelles formes pour refléter la croissance personnelle de leurs utilisateurs.",
        "image_url": "images/theories/kakyoin is stone free.jpg"
    },
    {
        "title": "Josuke s'est déplacé dans le temps pour se sauver bébé",
        "content": "Cette théorie propose que le mystérieux sauveur de Josuke lorsqu'il était bébé n'était autre qu'une version plus âgée de lui-même ayant voyagé dans le temps. Cela soulève des questions fascinantes sur la manipulation du temps et le rôle du destin dans l'univers de JoJo, tout en renforçant l'idée que les Joestar sont toujours liés par un sens profond de protection et de sacrifice.",
        "image_url": "images/theories/sauveur josuke.jpg"
    },
    {
        "title": "Star Platinum est Jonathan Joestar",
        "content": "Cette théorie postule que Star Platinum, le Stand de Jotaro Kujo, est en réalité l'esprit réincarné de Jonathan Joestar. Les similarités physiques et les capacités de Star Platinum rappellent le caractère noble et protecteur de Jonathan, suggérant qu'il continue de protéger sa famille au-delà de la mort. Cela pourrait également expliquer la force et la loyauté inébranlables de Star Platinum envers Jotaro.",
        "image_url": "images/theories/jonathan is star platinium.webp"
    },
    {
        "title": "La météorite des Flèches est faite des restes de Kars",
        "content": "Une théorie captivante avance que les Flèches, qui permettent aux humains d'éveiller leurs Stands, proviendraient d'une météorite formée à partir des restes de Kars. Après avoir été expulsé dans l'espace, Kars aurait été transformé en matière cosmique, infusant la météorite d'une énergie spéciale. Cela expliquerait l'origine surnaturelle et puissante des Flèches.",
        "image_url": "images/theories/ArcEtFleche.PNG.webp"
    },
    {
        "title": "Dio a planifié sa propre mort avec Pucci",
        "content": "Selon cette théorie, Dio aurait élaboré un plan complexe avec l'aide de son fidèle disciple, Enrico Pucci, pour orchestrer sa propre mort. L'objectif serait de manipuler les événements afin de préparer la création de Made in Heaven et de remodeler l'univers selon sa volonté. Cette théorie met en lumière la profondeur et l'ampleur des machinations de Dio, soulignant son obsession pour atteindre une domination ultime.",
        "image_url": "images/theories/Pucci_avec_DIO.webp"
    },
    {
        "title": "L'Arrow Requiem a choisi Giorno intentionnellement",
        "content": "Cette théorie propose que l'Arrow Requiem possède une conscience propre et a choisi Giorno Giovanna en raison de son incroyable potentiel et de sa détermination à apporter un changement positif. La théorie explore l'idée que l'Arrow agit comme un catalyseur spirituel, recherchant des individus capables d'utiliser son pouvoir pour des objectifs transcendants.",
        "image_url": "images/theories/la fleche a choisi giorno.jpg"
    },
    {
        "title": "Le Spin de Johnny est une évolution spirituelle", 
        "content": "Le Spin, une technique unique utilisée par Johnny Joestar, est présenté comme une manifestation de sa résilience spirituelle et de son développement personnel. Cette théorie examine comment le Spin transcende les simples lois de la physique, devenant une représentation symbolique de la détermination et de la quête de Johnny pour surmonter les défis et redéfinir son destin.",
        "image_url": "images/theories/spin de johnny.jpg"
    },
    {
        "title": "Les Stands sont hérités génétiquement",
        "content": "Une théorie populaire suggère que les Stands, bien qu'éveillés par des facteurs extérieurs comme les Flèches, sont en réalité un trait génétique transmis dans le sang de la famille Joestar. Cela expliquerait pourquoi tant de membres de cette lignée possèdent des Stands, et comment ces pouvoirs semblent évoluer pour s'adapter aux besoins et aux défis de chaque génération.", 
        "image_url": "images/theories/heritage stand.png"
    },
    {
        "title": "Les Piliers étaient des précurseurs des Stands",
        "content": "Selon cette théorie, les Hommes du Pilier, avec leurs capacités surhumaines et leur connexion au surnaturel, pourraient représenter une forme primitive des Stands. Leur existence antérieure à l'éveil des Stands suggère une évolution progressive des pouvoirs mystiques dans l'univers de JoJo, offrant un pont fascinant entre les premières générations et les aventures modernes.",
        "image_url": "images/theories/homme du pillier.jpg"
    }
]

   for i, theory_data in enumerate(theories_data, 1):
       theory, created = Theory.objects.get_or_create(
           title=theory_data["title"],
           defaults={
               "content": theory_data["content"],
               "user": admin_user,
               "image_url": theory_data["image_url"]
           }
       )
       if created:
           print(f"Théorie {i} créée : {theory.title}")
       else:
           print(f"Théorie {i} existe déjà : {theory.title}")
