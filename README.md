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

Utilisateur : patrick

Mot de passe : patrick

Voici les endpoints disponibles dans l'application :
### Résumé détaillé des projets
- GET : http://127.0.0.1:8000/api/projects/project_summary/

### Utilisateurs
- POST /users/ : Créer un utilisateur
- GET /users/ : Lister les utilisateurs
- PUT /users/{id}/ : Mettre à jour un utilisateur
- DELETE /users/{id}/ : Supprimer un utilisateur
- DELETE /users/{id}/delete_user/ : Supprimer un utilisateur avec suppression des projets et contributions

### Projets
- POST /projects/ : Créer un projet
- GET /projects/ : Lister les projets
- PUT /projects/{id}/ : Mettre à jour un projet
- DELETE /projects/{id}/ : Supprimer un projet

### Contributeurs
- POST /contributors/ : Ajouter un contributeur
- GET /contributors/ : Lister les contributeurs
- DELETE /contributors/remove_contributor/ : Retirer un contributeur d'un projet

### Issues
- POST /issues/ : Créer une issue
- GET /issues/ : Lister les issues
- PUT /issues/{id}/ : Mettre à jour une issue
- DELETE /issues/{id}/ : Supprimer une issue

### Commentaires
- POST /comments/ : Ajouter un commentaire
- GET /comments/ : Lister les commentaires
- PUT /comments/{id}/ : Mettre à jour un commentaire
- DELETE /comments/{id}/ : Supprimer un commentaire

## Auteur
Charron Emilie
