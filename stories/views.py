
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from stories.models import Story, Text
from stories.serializers import StorySerializer, TextSerializer


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


    def perform_create(self, serializer):
        try: 
            
        
                serializer.save(author=self.request.user)
            
        except:
            raise PermissionDenied("Not logged in users do not have permission to create an story.")
   

    def perform_update(self, serializer):
        try:
            if serializer.author == self.request.user:
                serializer.save(author=self.request.user)
        except AttributeError:
            raise PermissionDenied("You do not have permission to edit this.")

    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this story.")


class TextViewSet(viewsets.ModelViewSet):
    serializer_class = TextSerializer
    
    def perform_destroy(self, instance):
        if instance.story.author == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this story.")
        
    

    def perform_update(self, serializer):
        try:
            if serializer.story.author == self.request.user:
                serializer.save()
        except AttributeError:
            raise PermissionDenied("You do not have permission to edit this.")
    
    def get_queryset(self):
        # Get the story_id from the URL parameter
        story_id = self.kwargs.get('story_id')

        queryset = Text.objects.filter(story__id=story_id)

        return queryset

    def perform_create(self, serializer):
        story_id = self.kwargs.get('story_id')
        story = Story.objects.filter(id=story_id).first()
        
        if story != None:
            if story.author != self.request.user:
                raise PermissionDenied("You do not have permission to change any of this story.")
            

        serializer.save(story_id=story_id)
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Filter the queryset to get the root text (no previous_text)
        root_text = queryset.filter(previous_text__isnull=True).first()
        
        # Serialize the entire text tree starting from the root text
        serialized_tree = self.serialize_text_tree(root_text)

        return Response(serialized_tree)

    def serialize_text_tree(self, text):
        serialized_text = TextSerializer(text).data

        # Recursively serialize the next texts (text tree)
        choices = text.choices.all()
        if choices:
            serialized_text['choices'] = [
                self.serialize_text_tree(choice) for choice in choices
            ]

        return serialized_text