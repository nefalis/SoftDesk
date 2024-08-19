from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.password_validation import validate_password
from .models import User, Project, Contributor, Issue, Comment


class UserSerializer(serializers.ModelSerializer):
    # Le mot de passe est uniquement pour l'ecriture et ne sera pas affiché
    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password]
        )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'age',
            'email',
            'password',
            'can_be_contacted',
            'can_data_be_shared'
            ]

    def validate_email(self, value):
        # Vérifie si l'email existe déjà pour un autre utilisateur
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Un utilisateur avec cet email existe déjà"
                )
        return value

    def create(self, validated_data):
        # Crée un nouvel utilisateur avec le mot de passe haché.
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        # Met à jour un utilisateur et hache le mot de passe s'il est fourni
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'type',
            'author',
            'contributors',
            'time_created'
        ]

    def get_contributors(self, obj):
        # Retourne la liste des contributeurs associés au projet
        contributors = obj.contributor_id.all()
        return [
            {'id': contributor.id, 'username': contributor.username}
            for contributor in contributors
            ]

    def get_author(self, obj):
        # Retourne l'auteur du projet
        return {'id': obj.author_id.id, 'username': obj.author_id.username}

    def create(self, validated_data):
        # Récupérer l'utilisateur authentifié
        user = self.context['request'].user
        validated_data.pop('author_id', None)

        # Créer le projet avec l'utilisateur comme auteur
        project = Project.objects.create(author_id=user, **validated_data)

        # Ajouter les contributeurs au projet
        contributors_data = self.initial_data.get('contributors', [])
        for contributor_id in contributors_data:
            contributor = User.objects.get(id=contributor_id)
            Contributor.objects.create(user_id=contributor, project_id=project)

        return project


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user_id.username', read_only=True)
    project = serializers.CharField(source='project_id.title', read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'user_id', 'project_id']
        extra_kwargs = {
            'user_id': {'write_only': True},
            'project_id': {'write_only': True}
        }

    def validate(self, data):
        # Vérifie que l'utilisateur n'est pas déjà contributeur de ce projet
        user_id = self.initial_data.get('user_id')
        project_id = self.initial_data.get('project_id')

        if Contributor.objects.filter(
            user_id=user_id, project_id=project_id
        ).exists():
            raise serializers.ValidationError(
                "Cet utilisateur est déjà contributeur dans ce projet"
            )
        return data

    def create(self, validated_data):
        # Crée un nouveau contributeur pour le projet
        user = validated_data.get('user_id')
        project = validated_data.get('project_id')
        return Contributor.objects.create(user_id=user, project_id=project)


class IssueSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author_id.username', read_only=True
        )
    project_name = serializers.CharField(
        source='project_id.title', read_only=True
        )

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'author_id',
            'author_name',
            'project_id',
            'project_name',
            'status',
            'priority',
            'tag',
            'time_created'
        ]
        read_only_fields = ['author_id', 'author_name', 'project_name']

    def validate(self, data):
        # Vérifier que l'utilisateur est un contributeur du projet
        project = data.get('project_id')
        user = self.context['request'].user
        if not Contributor.objects.filter(
            project_id=project, user_id=user
        ).exists():
            raise serializers.ValidationError(
                "Vous devez être contributeur du projet"
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author_id.username', read_only=True
        )
    issue_title = serializers.CharField(
        source='issue_id.title', read_only=True
        )
    issue_link = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'uuid',
            'description',
            'time_created',
            'author_id',
            'author_name',
            'issue_id',
            'issue_title',
            'issue_link'
        ]
        read_only_fields = ['author_id', 'author_name', 'issue_title']

    def get_issue_link(self, obj):
        request = self.context.get('request')
        issue_link = reverse(
            'issue-detail', kwargs={'pk': obj.issue_id.pk}, request=request
            )
        return issue_link

    def validate(self, data):
        user = self.context['request'].user
        issue = data.get('issue_id')

        # Vérifier que l'utilisateur est contributeur du projet lié à l'issue
        project = issue.project_id
        if not Contributor.objects.filter(
            project_id=project, user_id=user
        ).exists():
            raise serializers.ValidationError(
                "Vous devez être contributeur du projet pour commenter."
            )

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author_id'] = user
        return super().create(validated_data)


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author_id.username', read_only=True)
    contributors = serializers.SerializerMethodField()
    issues = IssueSerializer(many=True, read_only=True, source='issue_set')
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'type',
            'time_created',
            'author',
            'contributors',
            'issues',
            'comments'
            ]

    def get_contributors(self, obj):
        # Retourne les contributeurs du projet
        contributors = Contributor.objects.filter(project_id=obj.id)
        return [{
            "id": contrib.user_id.id,
            "username": contrib.user_id.username}
            for contrib in contributors]

    def get_comments(self, obj):
        # Retourne les commentaires associés aux issues du projet
        comments = Comment.objects.filter(issue_id__project_id=obj.id)
        return CommentSerializer(comments, many=True).data
