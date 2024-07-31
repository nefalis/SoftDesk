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
    
    """
    def has_permission(self, request, view):
        # Assume view has project_id parameter or a similar way to get the project
        project_id = view.kwargs.get('project_id') or view.kwargs.get('pk')
        if not project_id:
            return False
        project = Project.objects.get(pk=project_id)
        return Contributor.objects.filter(project_id=project, user_id=request.user).exists()
    
