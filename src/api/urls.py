from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    ContributorViewSet, CommentViewSet, IssueViewSet
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
    )


router = DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('contributors', ContributorViewSet)
router.register('issues', IssueViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
