from django.contrib import admin
from .models import User, Contributor, Project, Issue, Comment

admin.site.register(User)
admin.site.register(Contributor)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
