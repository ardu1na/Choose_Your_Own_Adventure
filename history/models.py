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
    about = models.CharField(max_length=800, blank=True, null= True)

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="histories")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,  related_name="histories", verbose_name="author")
    
    version = models.DecimalField(default=1, max_digits=4, decimal_places=1, editable=False)
    
    published = models.BooleanField(default=False)
    
    has_changes = models.BooleanField(default=False)
    has_big_changes = models.BooleanField(default=False)
    
        
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

    @property
    def is_saved(self):
        for choice in self.texts.all():
            if choice.saved.exists():
                return True
            
            
    def __str__ (self):
        return f'{self.title} {self.version}'
    
    
    


class Saved(BaseModel):
    player = models.ForeignKey(Profile, related_name="saved", on_delete=models.CASCADE)
    stage = models.ForeignKey('Text', related_name="saved", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    
    # TODO: is current version
    
    def __str__ (self):
        return f'{self.player.user.username} played {self.stage.history.title} (saved)'
    
    
class Like(BaseModel):
    user = models.ForeignKey(Profile, related_name="likes", on_delete=models.CASCADE)
    history = models.ForeignKey(History, related_name="likes", on_delete=models.CASCADE)
    def __str__ (self):
        return f'{self.user.user.username} liked {self.history.title}'


class Text(BaseModel):
    
    history = models.ForeignKey(History, on_delete=models.CASCADE,  related_name="texts", null=True, blank=True)

    previous_text = models.ForeignKey('Text', on_delete=models.CASCADE,  related_name="choices", blank=True, null=True)
    
    option = models.CharField(max_length=600, null=True, blank=True)
 
    text = models.TextField(null=True, blank=True)
    
    
        
    def __str__ (self):
        return self.option if self.option else self.history.title
    
    @property
    def get_history_title (self):
        return self.history.title
    
    @property
    def is_start (self):
        if self.option == None:
            return True
    
    @property
    def is_end(self):
        history = History.objects.get(pk=self.history.pk)
        for choice in history.text.all():
            if choice.previous_text == self:
                return False
        return True
    
    @property
    def is_saved(self):
        history = History.objects.get(pk=self.history.pk)
        for choice in history.texts.all():
            if choice.saved.exists():
                return True
            
            
    @property
    def previous_option(self):
        return self.previous_text if self.previous_text else "inicio de la historia"
    
    
    # TODO: EN SAVE AJUSTAR PARAMETRO HISTORIA AUTOMATICAMENTE