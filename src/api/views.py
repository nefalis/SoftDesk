from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer, ContributorSerializer,
    IssueSerializer, CommentSerializer, ProjectDetailSerializer
    )
from api_user.models import User
from .permissions import ProjectPermission, ContributorPermission


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Vue pour gérer les projets : création,
    mise à jour, suppression, et récupération
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def perform_create(self, serializer):
        """
        Associe l'utilisateur authentifié
        comme auteur du projet lors de sa création
        """
        serializer.save(author_id=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def project_summary(self, request):
        """
        Retourne un résumé paginé de tous les projets
        """
        paginator = PageNumberPagination()
        paginator.page_size = 10
        projects = Project.objects.all()
        result_page = paginator.paginate_queryset(projects, request)
        serializer = ProjectDetailSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Vue pour gérer les contributeurs : ajout, suppression, etc
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Ajoute un contributeur à un projet,
        uniquement si l'utilisateur est l'auteur du projet
        """
        project_id = request.data.get('project_id')
        project = Project.objects.get(pk=project_id)

        # Vérifier que l'utilisateur est bien l'auteur du projet
        if project.author_id != request.user:
            return Response(
                {
                    'detail': (
                        "Vous n'êtes pas autorisé à "
                        "ajouter des contributeurs à ce projet"
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Si l'utilisateur est l'auteur, crée le contributeur
        return super().create(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['delete'],
        permission_classes=[IsAuthenticated, ProjectPermission]
    )
    def remove_contributor(self, request):
        """
        Supprime un contributeur d'un projet,
        uniquement si l'utilisateur est l'auteur du projet
        """
        user_id = request.data.get('user_id')
        project_id = request.data.get('project_id')

        # Vérifie l'existence de l'utilisateur et du projet
        user = User.objects.get(pk=user_id)
        project = Project.objects.get(pk=project_id)

        # Vérifier que l'utilisateur est bien l'auteur du projet
        if project.author_id != request.user:
            return Response(
                {
                    'detail': (
                        "Vous n'êtes pas autorisé à supprimer "
                        "des contributeurs de ce projet"
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Vérifie l'existence du contributeur à supprimer
        contributor = Contributor.objects.get(project_id=project, user_id=user)

        # Supprime le contributeur
        contributor.delete()
        return Response(
            {'status': 'Contributeur supprimé'},
            status=status.HTTP_204_NO_CONTENT
        )


class IssueViewSet(viewsets.ModelViewSet):
    """
    Vue pour gérer les issues : création,
    mise à jour, suppression, et récupération
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, ContributorPermission]

    def perform_create(self, serializer):
        """
        Associe l'utilisateur courant comme
        auteur de l'issue lors de sa création
        """
        serializer.save(author_id=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Vue pour gérer les commentaires : création,
    mise à jour, suppression, et récupération
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ContributorPermission]

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user)


class ProjectListView(generics.ListAPIView):
    """
    Vue pour lister tous les projets
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
