from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    
    def __str__ (self):
        return self.user.get_username()
    

class Genre(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__ (self):
        return self.name

class History(models.Model):
    
    title = models.CharField(max_length=150)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="histories")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,  related_name="histories")
    version = models.DecimalField(default=1, max_digits=4, decimal_places=2)
    published = models.BooleanField(default=False)
    
    @property
    def get_likes(self):
        likes = self.likes.all()
        return likes.count()
        
    def __str__ (self):
        return self.title
    


class Saved(models.Model):
    user = models.ForeignKey(Profile, related_name="saved_histories", on_delete=models.CASCADE)
    history = models.ForeignKey(History, related_name="saved_histories", on_delete=models.CASCADE)
    stage = models.ForeignKey('TextHistory', related_name="saved_histories", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    
    def __str__ (self):
        return f'{self.user.user.username} played {self.history.title} (saved)'
    
class Like(models.Model):
    user = models.ForeignKey(Profile, related_name="likes", on_delete=models.CASCADE)
    history = models.ForeignKey(History, related_name="likes", on_delete=models.CASCADE)
    def __str__ (self):
        return f'{self.user.user.username} liked {self.history.title}'


class TextHistory(models.Model):
    
    history = models.ForeignKey(History, on_delete=models.CASCADE,  related_name="texts", null=True, blank=True)

    text = models.TextField(null=True, blank=True)
    
    
    def __str__ (self):
        return self.text
    
    
    
class Choice(models.Model):
   
    option = models.CharField(max_length=500)
    
    previous_text = models.ForeignKey(TextHistory, on_delete=models.CASCADE,  related_name="choices")
    next_text = models.OneToOneField(TextHistory, on_delete=models.CASCADE,  related_name="choice")

    def __str__ (self):
        return self.option
    
    @property
    def get_history_title (self):
        return self.previous_text.history.title