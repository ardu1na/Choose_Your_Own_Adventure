from rest_framework import serializers

from stories.models import Story, Text, Genre
from users.models import CustomUser

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'  


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','id'] 



class TextSerializer(serializers.ModelSerializer):

    class Meta:
        model = Text
        exclude = ['date_updated','date_created','story']

    choices = serializers.SerializerMethodField()

    def get_choices(self, obj):
        choices = Text.objects.filter(previous_text=obj)
        return TextSerializer(choices, many=True).data

    
    
    
class StorySerializer(serializers.ModelSerializer):
    genre_data = GenreSerializer(source='genre', read_only=True)
    author_data = AuthorSerializer(source='author', read_only=True)
    class Meta:
        model = Story
        exclude = ['has_changes','has_big_changes','is_current_version','date_updated','date_created']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genre'] = data.pop('genre_data')
        data['author'] = data.pop('author_data')
        return data
    
    
