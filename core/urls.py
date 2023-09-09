
from django.contrib import admin
from rest_framework.routers import SimpleRouter
from django.urls import path, include
from stories.views import StoryViewSet, TextViewSet

story_router = SimpleRouter()
story_router.register(r'stories', StoryViewSet, basename='story')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(story_router.urls)),  

    path('api/stories/<int:story_id>/texts/', TextViewSet.as_view({'get': 'list', 'post': 'create'}), name='story-texts'),
    path('api/stories/<int:story_id>/texts/<int:pk>/', TextViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='story-text-detail'),
]
