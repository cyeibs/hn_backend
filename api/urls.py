from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, StoryListViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'list', StoryListViewSet, basename='story-list')

urlpatterns = [
    path('', include(router.urls)),
]

