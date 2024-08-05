from rest_framework import serializers
from .models import User, Project, Contributor, Issue, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'email', 'can_be_contacted', 'can_data_be_shared']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class ProjectSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author_id.username', read_only=True)
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'author', 'type', 'contributors', 'time_created']

    def get_contributors(self, obj):
        contributors = Contributor.objects.filter(project_id=obj.id)
        return [contrib.user_id.username for contrib in contributors]


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
    contributor = serializers.CharField(source='contributor_id.user_id.username', read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'priority', 'tag', 'time_created', 'contributor', 'comments']

    def get_comments(self, obj):
        comments = Comment.objects.filter(issue_id=obj.id)
        return CommentSerializer(comments, many=True).data
    
class CommentSerializer(serializers.ModelSerializer):
    contributor = serializers.CharField(source='contributor_id.user_id.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'time_created', 'contributor']


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author_id.username', read_only=True)
    contributors = serializers.SerializerMethodField()
    issues = IssueSerializer(many=True, read_only=True, source='issue_set')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'time_created', 'author', 'contributors', 'issues']

    def get_contributors(self, obj):
        contributors = Contributor.objects.filter(project_id=obj.id)
        return [contrib.user_id.username for contrib in contributors]