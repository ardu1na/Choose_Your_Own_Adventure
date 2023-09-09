from decimal import Decimal, ROUND_DOWN
from django.db import models
from users.models import CustomUser

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        abstract = True
        
           

class Genre(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__ (self):
        return self.name

class Story(BaseModel):
    
    title = models.CharField(max_length=150)
    about = models.CharField(max_length=800, blank=True, null= True)

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="stories")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  related_name="stories", verbose_name="author")
    
    version = models.DecimalField(default=1, max_digits=4, decimal_places=1, editable=False)
    
    published = models.BooleanField(default=False)
    
    has_changes = models.BooleanField(default=False)
    has_big_changes = models.BooleanField(default=False)
    
    is_current_version = models.BooleanField(default=True)
    
    @property
    def need_duplicate(self):
        if self.pk and self.published and self.is_saved:
            return True
    
    
    
    @property
    def big_changes_new_version(self):
        version = self.version.quantize(Decimal('1.'), rounding=ROUND_DOWN)
        new_version = version + 1
        return new_version
    
    
    
    @property
    def small_changes_new_version(self):
        if self.has_changes:
            new_version = self.version + Decimal(0.1)   
            return new_version
                
      
      
    
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
    player = models.ForeignKey(CustomUser, related_name="saved", on_delete=models.CASCADE)
    stage = models.ForeignKey('Text', related_name="saved", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    version = models.DecimalField(default=1, max_digits=4, decimal_places=1)
    
    def save(self, *args, **kwargs):
        self.version = self.stage.story.version
        super().save(*args, **kwargs)
    
    
    def __str__ (self):
        return f'{self.player.user.username} played {self.stage.story.title} (saved)'


    @property
    def is_current_version(self):
        return self.stage.story.is_current_version





    
    
class Like(BaseModel):
    user = models.ForeignKey(CustomUser, related_name="likes", on_delete=models.CASCADE)
    story = models.ForeignKey(Story, related_name="likes", on_delete=models.CASCADE)
    def __str__ (self):
        return f'{self.user.user.username} liked {self.story.title}'




    
class Rate(BaseModel):
    RATE_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),

        ]
    rate = models.CharField(max_length=15, null=False, blank=False, choices=RATE_CHOICES)
    user = models.ForeignKey(CustomUser, related_name="rated_stories", on_delete=models.CASCADE)
    story = models.ForeignKey(Story, related_name="rates", on_delete=models.CASCADE)
    def __str__ (self):
        return f'{self.user.user.username} rated {self.story.title}'


    
class Comment(BaseModel):
    comment = models.TextField()
    user = models.ForeignKey(CustomUser, related_name="comments", on_delete=models.CASCADE)
    story = models.ForeignKey(Story, related_name="comments", on_delete=models.CASCADE)
    def __str__ (self):
        return f'{self.user.user.username} commeted {self.story.title}'






class Text(BaseModel):
    
    story = models.ForeignKey(Story, on_delete=models.CASCADE,  related_name="texts", null=True, blank=True)

    previous_text = models.ForeignKey('Text', on_delete=models.CASCADE,  related_name="choices", blank=True, null=True)
    
    option = models.CharField(max_length=600, null=True, blank=True)
 
    text = models.TextField(null=True, blank=True)
    
    
        
    def __str__ (self):
        return self.option if self.option else self.story_title
    
    @property
    def story_title (self):
        return self.story.title
    
    @property
    def is_start (self):
        if self.option == None:
            return True
    
    @property
    def is_end(self):
        story = Story.objects.get(pk=self.story.pk)
        for choice in story.text.all():
            if choice.previous_text == self:
                return False
        return True
    
    @property
    def is_saved(self):
        story = Story.objects.get(pk=self.story.pk)
        for choice in story.texts.all():
            if choice.saved.exists():
                return True
            
            
    @property
    def previous_option(self):
        if self.is_start:
            return "Start"
        else:
            return self.previous_text
    
    
    @property
    def need_duplicate(self):
        if self.story and self.story.published and self.story.is_saved:
            return True
    
