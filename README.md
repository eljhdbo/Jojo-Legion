# Jojo Legion
## Contexte :

Dans le cadre d’un projet scolaire, nous avons développé un site web dédié à l’univers de JoJo’s Bizarre Adventure. Ce projet avait pour objectif principal d’apprendre à utiliser une API dans un contexte concret, en exploitant Django pour concevoir un site web fonctionnel tout en respectant les principes d’un développement structuré.

Le site propose une exploration de l’univers de JoJo, répertoriant prés de 170 personnages, classés par parties et récupérés via l’API "Jikan", qui s’appuie sur le celebre MyAnimeList. Le site inclut également des théories sur le manga ajouté minutieusement par les admin, un système de classement des personnages basé sur les likes, ainsi qu’une section permettant aux utilisateurs de consulter leurs likes.

---

## Guide des Fonctionnalités

### 1. Système d'Authentification
- **Localisation** : `views.py` - fonctions `login_view()`, `logout_view()`, `register_view()`
- **Modèle** : `models.py` - classe `User` avec rôles personnalisés
- Permet l'inscription, la connexion et la déconnexion des utilisateurs

### 2. Gestion des Personnages
- **API et Import** : `views.py` - fonction `fetch_and_store_jojo_data()`
  - Récupère automatiquement les personnages depuis l'API Jikan
  - Classe les personnages par parties
- **Affichage** : `views.py` - fonction `list_characters()`
- **Modèles** : `models.py` - classes `Character` et `Part`

### 3. Système de Likes
- **Pour les Personnages** :
  - **Vue** : `views.py` - fonction `like_character()`
  - **Modèle** : `models.py` - classe `CharacterLike`
- **Pour les Théories** :
  - **Vue** : `views.py` - fonction `like_theory()`
  - **Modèle** : `models.py` - classe `ArchivedLike`

### 4. Gestion des Théories
- **Affichage** : `views.py` - fonction `list_theories()`
- **Modèle** : `models.py` - classe `Theory`
- Permet aux utilisateurs de consulter les théories sur l'univers JoJo

### 5. Système de Classement
- **Vue** : `views.py` - fonction `rankings()`
- Affiche le top 10 des personnages et théories les plus appréciés
- Utilise les compteurs de likes des modèles `Character` et `Theory`

### 6. Section Personnelle
- **Vue** : `views.py` - fonction `my_likes()`
- Permet aux utilisateurs de voir leurs personnages et théories favoris



## Installation et paramettrage

### Prérequis (logiciel)

1. **Un IDE** : Nous recommandons [Visual Studio Code](https://code.visualstudio.com/) car il est simple à prendre en main, très pratique pour organiser son code, et parfait pour apprendre.
2. **Python** : Installez [Python](https://www.python.org/downloads/) la version 3.8 ou plus. Django, étant un Framework basé sur Python, ce langage est donc nécessaire.
3. **Django** : Installez Django avec cette commande dans le terminal :
   ```bash
   pip install django
   ```
4. **Bibliothèque Requests** : Cette bibliothèque va nous permet de faire des requêtes HTTP facilement, ce qui est essentiel pour interagir avec des API comme "Jikan". Installez-la avec la commande suivante :
   ```bash
   pip install requests
   ```
   Une fois installée, vous pourrez, par exemple, récupérer des données en utilisant :
   ```python
   import requests

   response = requests.get('https://api.jikan.moe/v4/characters')
   print(response.json())
   ```

### Guide d'installation/Commandes à exécuter

1. Clonez le dépôt du projet :
   ```bash
   git clone https://github.com/eljhdbo/Jojo-Legion.git
   cd jojo-site
   ```
2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```
3. Ajoutez les theories p :
   ```bash
   python manage.py add_theories
   ```

## lancer le serveur

1. **Démarrez le serveur local** :
   ```bash
   python manage.py runserver
   ```
2. **Accéder à l'URL du site** :  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/) et ajouter `/fetch-data/`  
comme cela : [http://127.0.0.1:8000/fetch-data/](http://127.0.0.1:8000/fetch-data/)  

Par la suite, un message comme ceci indique que les persos ont été ajoutés :  

{
  "message": "Données récupérées et stockées avec succès !"
}

## vous pouvez désormais utilisez JoJo Legion !

---

## La base de données

Le projet utilise une base de données SQLite qui est la base de données par défaut de Django.

- **Emplacement du fichier** : `db.sqlite3`
- **Gestion des données** : Django ORM offre une interface puissante et facile d’accès pour manipuler les modèles de personnages et de théories.

Pour accéder directement aux données ou les manipuler, utilisez la commande suivante :

```bash
python manage.py shell
```
