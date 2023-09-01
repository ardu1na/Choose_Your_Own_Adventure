from django.db import models
from django.contrib.auth.models import User



class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        abstract = True
        
        

class Profile(BaseModel):
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

class History(BaseModel):
    
    title = models.CharField(max_length=150)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="histories")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,  related_name="histories", verbose_name="author")
    
    version = models.DecimalField(default=1, max_digits=4, decimal_places=2, editable=False)
    old = models.BooleanField(default=False) 
    published = models.BooleanField(default=False)
    
        
    @property
    def get_likes(self):
        likes = self.likes.all()
        return likes.count()
    
    @property
    def get_users_who_liked(self):
        likes = self.likes.all()
        users = []
        for like in likes:
            users.append(like.user)
            
        return users
        
    def __str__ (self):
        return f'{self.title} (V: {self.version})'
    
    def save(self, *args, **kwargs):
        if self.pk and self.published == True and self.saved_histories.exists():
             
            print("historia jugada x usuarios y publicada que debe ser clonada y con una nueva versión")
            new_version = self.version + 1
            new_version = History.objects.create(
                title=self.title,
                genre=self.genre,
                user=self.user,
                version = new_version,
                published = False)
            
            self.old = True
            self.published = False
            
        super().save(*args, **kwargs)

    


class Saved(BaseModel):
    user = models.ForeignKey(Profile, related_name="saved_histories", on_delete=models.CASCADE)
    history = models.ForeignKey(History, related_name="saved_histories", on_delete=models.CASCADE)
    stage = models.ForeignKey('TextHistory', related_name="saved_histories", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    
    def __str__ (self):
        return f'{self.user.user.username} played {self.history.title} (saved)'
    
class Like(BaseModel):
    user = models.ForeignKey(Profile, related_name="likes", on_delete=models.CASCADE)
    history = models.ForeignKey(History, related_name="likes", on_delete=models.CASCADE)
    def __str__ (self):
        return f'{self.user.user.username} liked {self.history.title}'


class TextHistory(BaseModel):
    
    history = models.ForeignKey(History, on_delete=models.CASCADE,  related_name="texts", null=True, blank=True)

    text = models.TextField(null=True, blank=True)
    
    def previous(self):
        if self.choice:
            return self.choice
        else:
            return 'First Chapter'
    
    def __str__ (self):
        return self.text
    
    
    
class Choice(BaseModel):
   
    option = models.CharField(max_length=500)
    
    previous_text = models.ForeignKey(TextHistory, on_delete=models.CASCADE,  related_name="choices")
    next_text = models.OneToOneField(TextHistory, on_delete=models.CASCADE,  related_name="choice")

    def __str__ (self):
        return self.option
    
    @property
    def get_history_title (self):
        return self.previous_text.history.title