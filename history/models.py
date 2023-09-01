from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    def __str__ (self):
        return self.user.get_username()
    
"""
Las historias tienen título, Genero, y referencia de textblocks
Los textblocks tienen: Text, Choices.
Las choices tienen: Text, NextText(solo 1 nextText por choice
"""    

class Genre(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__ (self):
        return self.name

class History(models.Model):
    
    
    title = models.CharField(max_length=150)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="histories")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,  related_name="histories")
    
    def __str__ (self):
        return self.title
    

    # time line. arrastar block text

class TextHistory(models.Model):
    
    history = models.ForeignKey(History, on_delete=models.CASCADE,  related_name="texts", null=True, blank=True)

    text = models.TextField(null=True, blank=True)
    
    
    def __str__ (self):
        return self.text
    
    
    
class Choices(models.Model):
    history = models.ForeignKey(History, on_delete=models.CASCADE,  related_name="choices")
    
    option = models.CharField(max_length=500)
    
    previous_text = models.ForeignKey(TextHistory, on_delete=models.CASCADE,  related_name="choices")
    next_text = models.OneToOneField(TextHistory, on_delete=models.CASCADE,  related_name="choice")

    def __str__ (self):
        return self.option