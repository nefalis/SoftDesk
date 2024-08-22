from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from api.models import Project, Contributor
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Vue pour gérer les utilisateurs : création, modification, suppression, etc
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # Droit à l'oubli
    @action(
        detail=True,
        methods=['delete'],
        permission_classes=[IsAuthenticated]
    )
    def delete_user(self, request, pk=None):
        """
        Supprime un utilisateur, ainsi que tous
        les projets et contributions associés
        """
        user = self.get_object()

        # Supprimer les projets où l'utilisateur est l'auteur
        Project.objects.filter(author_id=user).delete()

        # Supprimer les contributions de l'utilisateur
        Contributor.objects.filter(user_id=user).delete()

        # Supprimer l'utilisateur lui-même
        user.delete()

        return Response(
            {'status': 'Utilisateur supprimé'},
            status=status.HTTP_204_NO_CONTENT
        )
