from rest_framework import serializers
from .models import User, Project, Contributor, Issue, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'email','password', 'can_be_contacted', 'can_data_be_shared']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class ProjectSerializer(serializers.ModelSerializer):

    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    contributors_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'author_id', 'type', 'contributor_id', 'time_created']

    def create(self, validated_data):
        contributors = validated_data.pop('contributors', [])
        project = super().create(validated_data)

        # Ajout des contributeurs au projet
        for contributor in contributors:
            Contributor.objects.get_or_create(user_id=contributor, project_id=project)

        return project


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user_id.username', read_only=True)
    project = serializers.CharField(source='project_id.title', read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']

    def validate(self, data):
        if Contributor.objects.filter(user_id=data['user_id'], project_id=data['project_id']).exists():
            raise serializers.ValidationError("Cet utilisateur est déjà contributeur dans ce projet")
        return data
    
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'contributor_id', 'project_id', 'status', 'priority', 'tag', 'time_created']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'time_created', 'contributor_id', 'issue_id']

class ProjectDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author_id.username', read_only=True)
    contributors = serializers.SerializerMethodField()
    issues = IssueSerializer(many=True, read_only=True, source='issue_set')
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'time_created', 'author', 'contributors', 'issues', 'comments']

    def get_contributors(self, obj):
        contributors = Contributor.objects.filter(project_id=obj.id)
        return [{"id": contrib.user_id.id, "username": contrib.user_id.username} for contrib in contributors]

    def get_comments(self, obj):
        comments = Comment.objects.filter(issue_id__project_id=obj.id)
        return CommentSerializer(comments, many=True).data