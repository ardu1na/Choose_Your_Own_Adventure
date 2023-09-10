
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from stories.models import Story, Text,\
    Saved, Like
from stories.serializers import StorySerializer, TextSerializer,\
    SavedSerializer, LikeSerializer
    
    
class CloneStoryAPIView(APIView):
    def get(self, request, story_id, *args, **kwargs):
        try:
            story = Story.objects.filter(pk=story_id).first()
            
            if not story:
                return Response({'message': 'Story not found'}, status=status.HTTP_404_NOT_FOUND)
            if request.user == story.author:
                clon = story.clone_story()
                clon_serializer = StorySerializer(instance=clon)
                return Response({'message': 'Story cloned', 'cloned_story': clon_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message':'Not authorized user'}, status= status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
        
class SavedViewSet(viewsets.ModelViewSet):
    serializer_class = SavedSerializer

    def get_queryset(self):
        return Saved.objects.filter(player=self.request.user)

    
    def perform_create(self, serializer):
        try: 
            serializer.save(player=self.request.user)
        except:
            raise PermissionDenied("Permission denied")
   

    def perform_update(self, serializer):
        try:
            if serializer.player == self.request.user:
                serializer.save()
        except AttributeError:
            raise PermissionDenied("You do not have permission to do this.")

    def perform_destroy(self, instance):
        if instance.player == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this saved story.")



class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    
    def perform_create(self, serializer):
        try:
            # Set the 'user' field based on the 'request.user'
            serializer.save(user=self.request.user)
        except Exception as e:
            print(f"Error creating like: {str(e)}")

    def perform_update(self, serializer):
        
            raise PermissionDenied("You do not have permission to do this.")

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this like.")


class StoryViewSet(viewsets.ModelViewSet):
    """
        In order to go to story__texts use: api/stories/ < story__id > /texts
        Only logged in users can create stories.
        Only author can update or delete its own stories
    """
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
        
        
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
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        if not isinstance(serializer.instance, list):
            next_choices = [{'id': choice.id, 'option': choice.option} for choice in instance.choices.all()]
            
            response_data = {
                **serializer.data,
                'next_choices': next_choices,
            }
            
            return Response(response_data)
        return Response(serializer.data)



    def perform_update(self, serializer):
        try:
            if serializer.instance.story.author == self.request.user:
                serializer.save()
        except AttributeError:
            raise PermissionDenied(f"You do not have permission to edit this {self.request.user}")
    
    def get_queryset(self):
        # Get the story_id from the URL parameter
        story_id = self.kwargs.get('story_id')

        queryset = Text.objects.filter(story__id=story_id)

        return queryset

    def perform_create(self, serializer):
        story_id = self.kwargs.get('story_id')
        story = Story.objects.filter(id=story_id).first()

        if story is not None:
            if story.author != self.request.user:
                raise PermissionDenied("You do not have permission to change any of this story.")

        serializer.save(story_id=story_id)


        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Filter the queryset to get the root text (no previous_text)
        root_text = queryset.filter(previous_text__isnull=True).first()
        
        if root_text is not None:
            # Serialize the entire text tree starting from the root text
            serialized_tree = self.serialize_text_tree(root_text)
            return Response(serialized_tree)
        else:
            # Handle the case when there are no instances in the history
            return Response([])
        
    def serialize_text_tree(self, text, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = []

        # Add 'previous_text' to the list of fields to exclude
        exclude_fields.append('previous_text')

        # Serialize the text
        serialized_text = TextSerializer(text).data

        # Exclude specified fields
        for field in exclude_fields:
            serialized_text.pop(field, None)

        # Recursively serialize the next texts (text tree)
        choices = text.choices.all()
        if choices:
            serialized_text['choices'] = [
                self.serialize_text_tree(choice, exclude_fields) for choice in choices
            ]

        return serialized_text

