# SoftDesk 
SoftDesk est une API de gestion de problèmes. Cet outil permet de faire remonter et de suivre des problèmes avec la création d'utilisateurs et de projets contenant des issues et des commentaires.

Fonctionnalités
- Gestion des utilisateurs (inscription, connexion, modification du mot de passe)
- Création, lecture, modification et suppression de projets
- Gestion des contributeurs dans les projets
- Création, lecture, modification et suppression des issues dans les projets
- Ajout et gestion des commentaires pour les issues
Les actions peuvent être tester à l'aide de Postman et les endpoints seront décrit plus bas.

Elle a été construite avec Django Rest Framework.

## Mise en place du projet
Pour ce projet, vous avez besoin d'avoir Python 🐍 d'installer sur votre ordinateur. Vous pouvez le télécharger depuis le site officiel de Python .


Créez un nouveau dossier sur votre bureau avec le nom que vous souhaitez
- Télécharger le contenu du projet ou clonez le avec le lien suivant :
```
https://github.com/nefalis/SoftDesk.git
```
- Installation de pipenv :
```
pip install pipenv
```
- Activation de l'environnement virtuel:
```
pipenv shell
```
- Metter vous dans le dossier softdesk :
```
cd softdesk 
```
- Effectuer les migrations de la base de données :
```
python manage.py migrate
```
- Lancement du serveur :
```
python manage.py runserver
```
## Utilisation de Postman
l'URL de base est la suivante : http://127.0.0.1:8000/api/

Afin de visualisé les informations, vous devez être connecté.
Voici un exemple d'utilisateur :

* Utilisateur : Robert

* Mot de passe : Tfe45+ef

* Utilisateur : Julie

* Mot de passe : 21Ju6+pm


Voici les endpoints disponibles dans l'application :
### Résumé détaillé des projets avec issue et commentaire
- GET : http://127.0.0.1:8000/api/projects/project_summary/

### Utilisateurs
- POST http://127.0.0.1:8000/api_user/users/ : Créer un utilisateur
- GET http://127.0.0.1:8000/api_user/users/ : Liste des utilisateurs
- PUT http://127.0.0.1:8000/api_user/users/{id}/ : Modifier un utilisateur
- DELETE http://127.0.0.1:8000/api_user/users/{id}/: Supprimer un utilisateur
- DELETE http://127.0.0.1:8000/api_user/users/{id}/delete_user/ : Supprimer un utilisateur avec suppression des projets et contributions
  -> droit a l'oubli

### Projets
- POST http://127.0.0.1:8000/api/projects/ : Créer un projet
- GET http://127.0.0.1:8000/api/projects/ : Liste des projets
- PUT http://127.0.0.1:8000/api/projets/{id}/ : Modifier un projet
- DELETE http://127.0.0.1:8000/api/projects/{id}/ : Supprimer un projet

### Contributeurs
- POST http://127.0.0.1:8000/api/contributors/ : Ajouter un contributeur
- GET http://127.0.0.1:8000/api/contributors/ : Liste des contributeurs
- DELETE http://127.0.0.1:8000/api/contributors/remove_contributor/ : Retirer un contributeur d'un projet

### Issues
- POST http://127.0.0.1:8000/api/issues/ : Créer une issue
- GET http://127.0.0.1:8000/api/issues/ : Liste des issues
- PUT http://127.0.0.1:8000/api/issues/{id}/ : Modifier une issue
- DELETE http://127.0.0.1:8000/api/issues/{id}/ : Supprimer une issue

### Commentaires
- POST /comments/ : Ajouter un commentaire
- GET http://127.0.0.1:8000/api/comments/ : Liste des commentaires
- PUT http://127.0.0.1:8000/api/comments/{id}/ : Modifier un commentaire
- DELETE http://127.0.0.1:8000/api/comments/{id}/ : Supprimer un commentaire

## Auteur
Charron Emilie
