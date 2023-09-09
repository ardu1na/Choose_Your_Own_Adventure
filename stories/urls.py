from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stories.views import TextViewSet, StoryViewSet

story_router = DefaultRouter()
story_router.register(r'stories', StoryViewSet)

text_router = DefaultRouter()
text_router.register(r'texts', TextViewSet)

urlpatterns = [
    path('api/', include(story_router.urls)), 
    path('api/stories/<int:story_id>/', include(text_router.urls)), 
]
