from rest_framework import serializers
from .models import User, Project, Contributor, Issue, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'email', 'password', 'can_be_contacted', 'can_data_be_shared']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class ProjectSerializer(serializers.ModelSerializer):

    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    contributor_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'author_id', 'type', 'contributor_id', 'time_created']

    def validate_contributor_id(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Ce contributeur est déjà dans ce projet.")
        return value


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id']

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