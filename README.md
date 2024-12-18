## Contexte :

Dans le cadre d'un projet scolaire stimulant, nous avons créé un site web sur le thème fascinant de JoJo’s Bizarre Adventure. L'objectif principal était de maîtriser Django pour concevoir une API fonctionnelle, tout en respectant les étapes d'un développement web bien structuré.

Ce site propose une plongée dans l'univers de JoJo, avec plus de 150 personnages emblématiques classés par parties, soigneusement extraits de l'API "Jikan" basée sur MyAnimeList. En plus, il offre des théories captivantes autour du manga, un classement des personnages via un système de likes, et une section personnalisée pour consulter ses propres interactions.

---

## les fonctionnalités : où les trouver dans le code ?

1. **Créer un compte** : Permet aux utilisateurs de s'inscrire et de se connecter pour une expérience personnalisée.

2. **Voir les personnages** : Accédez à une liste de plus de 150 personnages.

3. **Voir les théories** : Consultez des théories enrichissantes sur l'univers de JoJo.

4. **Liker des personnages et des théories** : Permet aux utilisateurs de marquer leurs personnages et théories préférés.

5. **Retrouver ses "likes"** : Une section dédiée "Mes Likes" regroupe tous les personnages et théories aimés par l'utilisateur.

6. **Voir le classement des personnages et des théories les plus aimés** : Une page dédiée pour visualiser les personnages et les théories les plus appréciés de la communauté.
---

## Installation et paramettrage

### Prérequis (logiciel)

1. **Un IDE performant** : Nous recommandons [Visual Studio Code](https://code.visualstudio.com/) car il est simple à prendre en main, très pratique pour organiser son code, et parfait pour apprendre.
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
2. Configurez un environnement virtuel :
   - **Sous Windows** :
     ```bash
     python -m venv env
     env\Scripts\activate
     ```
   - **Sous macOS/Linux** :
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```
3. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```
4. Appliquez les migrations pour initialiser la base de données :
   ```bash
   python manage.py migrate
   ```

### Configuration supplémentaire

Adaptez le fichier `settings.py` avec les paramètres de votre base de données ou toute clé API supplémentaire selon vos besoins.

---

## Pour un lancement rapide

1. **Démarrez le serveur local** :
   ```bash
   python manage.py runserver
   ```
2. **Testez l'API** (exemple avec Requests) :
   ```python
   import requests

   response = requests.get('http://127.0.0.1:8000/api/characters/')
   print(response.json())
   ```

---

## La base de données

Le projet utilise une base de données SQLite pour une gestion simplifiée et efficace.

- **Emplacement du fichier** : `db.sqlite3`
- **Gestion des données** : Django ORM offre une interface puissante et facile d’accès pour manipuler les modèles de personnages et de théories.

Pour accéder directement aux données ou les manipuler, utilisez la commande suivante :

```bash
python manage.py shell
```
