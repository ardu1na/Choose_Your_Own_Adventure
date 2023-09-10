
from django.contrib import admin
from django.urls import path, include

from stories.urls import urlpatterns
from stories.views import TextViewSet
...
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Choose Your Own Adventure API",
      default_version='v1',
      description="Beta version of endpoints",
      contact=openapi.Contact(email="arduinadelbosque@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/', include('stories.urls')),  

    path('api/stories/<int:story_id>/texts/', TextViewSet.as_view({'get': 'list', 'post': 'create'}), name='story-texts'),
    path('api/stories/<int:story_id>/texts/<int:pk>/', TextViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='story-text-detail'),
]
