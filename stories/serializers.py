from rest_framework import serializers

from stories.models import Story, Text, Genre,\
    Saved, Like
from users.models import CustomUser

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'  


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'  

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
    genre_data = GenreSerializer(source='genre', read_only=True)
    author = AuthorSerializer(source='customuser', read_only=True)
    likes = serializers.ReadOnlyField(source='get_likes')
    class Meta:
        model = Story
        exclude = ['date_updated', 'date_created']  

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genre'] = data.pop('genre_data')
        return data

    
