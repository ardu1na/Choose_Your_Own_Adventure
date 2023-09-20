from rest_framework import serializers

from stories.models import Story, Text, Genre,\
    Saved, Like
from users.models import CustomUser

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'  


class LikeSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField(source='datetime')

    class Meta:
        model = Like
        exclude = ['date_created',]

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','id'] 

    
    
    
class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        exclude = ['player', 'date_created']


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        exclude = ['date_updated','date_created','story']

    

class StorySerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source='author.id')
    author_username = serializers.ReadOnlyField(source='author.username')

    genre_data = GenreSerializer(source='genre', read_only=True)
    likes = serializers.ReadOnlyField(source='get_likes')
    created = serializers.ReadOnlyField(source='created_at')
    updated = serializers.ReadOnlyField(source='updated_at')

    class Meta:
        model = Story
        exclude = ['date_updated', 'date_created', 'author']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genre'] = data.pop('genre_data')
        data['author'] = {
            'author_id': data.pop('author_id'),
            'author_username': data.pop('author_username')
        }
        return data

