from rest_framework import permissions
from .models import Contributor, Issue, Comment


class ProjectPermission(permissions.BasePermission):
    """
    Cette permission restreint les actions de modification
    et de suppression d'un projet uniquement à l'auteur de
    ce projet. Les autres utilisateurs peuvent seulement consulter
    le projet.
    """

    def has_permission(self, request, view):
        # Vérifie que l'utilisateur est authentifié
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Autorise uniquement les méthodes de lecture (GET)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Autorise les actions d'écriture (PUT, DELETE) uniquement
        # si l'utilisateur est l'auteur du projet
        return obj.author_id == request.user


class ContributorPermission(permissions.BasePermission):
    """
    Cette permission vérifie si l'utilisateur est contributeur
    d'un projet donné. Les contributeurs peuvent consulter les
    informations et interagir avec les objets liés au projet.
    Les actions d'écriture sont limitées aux contributeurs du projet associé.
    """
    def has_permission(self, request, view):
        # Vérifie que l'utilisateur est authentifié
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Autorise uniquement les méthodes de lecture (GET)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Obtenez l'ID du projet selon que l'objet
        # est une "Issue", un "Comment", ou autre.
        if isinstance(obj, Issue):
            project_id = obj.project_id.id
        elif isinstance(obj, Comment):
            project_id = obj.issue_id.project_id.id
        else:
            project_id = view.kwargs.get('project_id')

        # Si aucun project_id n'est trouvé, l'accès est refusé
        if not project_id:
            return False

        # Vérifie si l'utilisateur est un contributeur du projet associé.
        return Contributor.objects.filter(
            project_id=project_id, user_id=request.user
            ).exists()
