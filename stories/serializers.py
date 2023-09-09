from rest_framework import serializers

from stories.models import Story, Text, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'  

class StorySerializer(serializers.ModelSerializer):
    genre_data = GenreSerializer(source='genre', read_only=True)

    class Meta:
        model = Story
        exclude = ['has_changes','has_big_changes','is_current_version','author','date_updated','date_created']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genre'] = data.pop('genre_data')
        return data

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'


