from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    age = models.PositiveSmallIntegerField(
        default=15,
        validators=[MinValueValidator(15)],
        verbose_name=("age")
    )
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def __str__(self):
        return self.username
