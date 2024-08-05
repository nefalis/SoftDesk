from rest_framework import permissions
from .models import User, Project, Contributor, Issue, Comment

class ProjectPermission(permissions.BasePermission):
    """
    permission pour qu'il n'y ai que l'auteur du projet qui puisse modifier ou supprimer
    """

    def has_permission(self, request, view):
        # verif que c'est bien l'auteur
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # permission de lecture uniquement
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # permission ecriture accordé qu'a l'auteur
        return obj.author_id == request.user
    

class ContributorPermission(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est contributeur du projet.
    """
    def has_permission(self, request, view):
        # Vérifie que l'utilisateur est authentifié
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Permission de lecture uniquement
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Pour les actions d'écriture, vérifiez si l'utilisateur est contributeur du projet associé
        if isinstance(obj, Issue):
            project_id = obj.project_id.id
        elif isinstance(obj, Comment):
            project_id = obj.issue_id.project_id.id
        else:
            project_id = view.kwargs.get('project_id')
        
        if not project_id:
            return False
        
        return Contributor.objects.filter(project_id=project_id, user_id=request.user).exists()