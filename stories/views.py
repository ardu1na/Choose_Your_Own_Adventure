from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from stories.models import Story, Text
from stories.serializers import StorySerializer, TextSerializer


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the author field to the current user when creating a story
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Set the author field to the current user when updating a story
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        # Ensure the user deleting the story is the author
        if instance.author == self.request.user:
            instance.delete()
        else:
            # You can raise a permission denied exception or handle it as needed
            raise PermissionDenied("You do not have permission to delete this story.")


class TextViewSet(viewsets.ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
