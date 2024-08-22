
from django.contrib.auth.models import User

user = User.objects.get(username='superuser')
print(user.username, user.email, user.is_active)