from django.contrib import admin
from django.urls import path, include
from api import urls as api_urls
from api_user import urls as api_user_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('api_user/', include(api_user_urls)),
]
