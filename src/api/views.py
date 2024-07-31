from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, Project, Contributor, Issue, Comment
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import ProjectPermission, ContributorPermission



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_contributor(self, request):
        user_id = request.data.get('user_id')
        project_id = request.data.get('project_id')
        try:
            user = User.objects.get(pk=user_id)
            project = Project.objects.get(pk=project_id)
            contributor = Contributor.objects.get(project_id=project, user_id=user)
            contributor.delete()
            return Response({'status': 'contributor removed'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response({'error': 'project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Contributor.DoesNotExist:
            return Response({'error': 'contributor not found'}, status=status.HTTP_404_NOT_FOUND)

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, ContributorPermission]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ContributorPermission]