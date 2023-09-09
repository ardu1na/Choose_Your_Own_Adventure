
from django.contrib import admin
from rest_framework.routers import SimpleRouter
from django.urls import path, include

from stories.urls import urlpatterns
from stories.views import TextViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('stories.urls')),  

    path('api/stories/<int:story_id>/texts/', TextViewSet.as_view({'get': 'list', 'post': 'create'}), name='story-texts'),
    path('api/stories/<int:story_id>/texts/<int:pk>/', TextViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='story-text-detail'),
]
