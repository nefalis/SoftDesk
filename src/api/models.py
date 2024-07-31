from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    age = models.PositiveSmallIntegerField(default=15, validators=[MinValueValidator(15)], verbose_name=("age"))
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Project(models.Model):
    title = models.CharField(max_length=155)
    description = models.TextField()
    type = models.CharField(max_length=12)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_id')
    contributor_id = models.ManyToManyField(User, through='Contributor')
    time_created = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        # pour eviter doublons contributeur dans projet
        unique_together = ('user_id', 'project_id')

class Issue(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    contributor_id = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    contributor_id = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
