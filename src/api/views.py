from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, Project, Contributor, Issue, Comment
from .serializers import (
    UserSerializer, ProjectSerializer, ContributorSerializer,
    IssueSerializer, CommentSerializer, ProjectDetailSerializer
    )
from .permissions import ProjectPermission, ContributorPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # Droit a l'oubli
    @action(
        detail=True,
        methods=['delete'],
        permission_classes=[IsAuthenticated]
        )
    def delete_user(self, request, pk=None):
        user = self.get_object()

        # Supprimer les projets où l'utilisateur est l'auteur
        Project.objects.filter(author_id=user).delete()

        # Supprimer les contributions de l'utilisateur
        Contributor.objects.filter(user_id=user).delete()

        # Supprimer l'utilisateur lui-même
        user.delete()

        return Response(
            {'status': 'user deleted'},
            status=status.HTTP_204_NO_CONTENT
            )


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
        )
    def project_summary(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        projects = Project.objects.all()
        result_page = paginator.paginate_queryset(projects, request)
        serializer = ProjectDetailSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Récupérer le project_id depuis les données de la requête
        project_id = request.data.get('project_id')
        project = Project.objects.get(pk=project_id)

        # Vérifier que l'utilisateur est bien l'auteur du projet
        if project.author_id != request.user:
            return Response(
                {'detail': "Vous n'êtes pas autorisé à ajouter des contributeurs à ce projet."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Si tout va bien, procéder à la création du contributeur
        return super().create(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['delete'],
        permission_classes=[IsAuthenticated, ProjectPermission]
        )
    def remove_contributor(self, request):
        user_id = request.data.get('user_id')
        project_id = request.data.get('project_id')

        # Verif que utilisateur et projet existent
        user = User.objects.get(pk=user_id)
        project = Project.objects.get(pk=project_id)

        # Vérifier que l'utilisateur est bien l'auteur du projet
        if project.author_id != request.user:
            return Response(
                {'detail': "Vous n'êtes pas autorisé à supprimer des contributeurs de ce projet."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # verif que le contributeur existe
        contributor = Contributor.objects.get(project_id=project, user_id=user)

        #suppriem contributeur
        contributor.delete()
        return Response(
            {'status': 'contributor removed'},
            status=status.HTTP_204_NO_CONTENT
            )


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, ContributorPermission]


    def perform_create(self, serializer):
        # Associer l'utilisateur courant comme auteur de l'issue
        serializer.save(author_id=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ContributorPermission]


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
