from rest_framework import serializers

from stories.models import Story, Text, Genre, Saved
from users.models import CustomUser

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'  


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','id'] 

    
    
    
class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        exclude = ['player',]


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        exclude = ['date_updated','date_created','story']

    


class StorySerializer(serializers.ModelSerializer):
    genre_data = GenreSerializer(source='genre', read_only=True)
    author = AuthorSerializer(source='customuser', read_only=True)
    
    
    class Meta:
        model = Story
        exclude = ['date_updated', 'date_created']  

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genre'] = data.pop('genre_data')
        return data

    
