from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


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
    request = self.context.get('request')
    if request and request.method == 'PUT':
        user_id = request.parser_context.get('kwargs', {}).get('pk')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                if user.email == value:
                    return value
            except User.DoesNotExist:
                pass

    # Vérifiez si l'email existe déjà pour un autre utilisateur
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
