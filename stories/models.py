from decimal import Decimal, ROUND_DOWN
from django.db import models
from rest_framework import exceptions

from users.models import CustomUser

######## UTILS
class TextChangeNotAllowed(exceptions.APIException):
    status_code = 400
    default_detail = "Cannot change this text because the story is already being played by users."
    default_code = "text_change_not_allowed"


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        abstract = True
        
           
######### MAIN
class Genre(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__ (self):
        return self.name



class Story(BaseModel):
    
    title = models.CharField(max_length=150)
    about = models.CharField(max_length=800, blank=True, null= True)

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="stories")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  related_name="stories", verbose_name="author")#, editable=False)
    
    version = models.DecimalField(default=1, max_digits=4, decimal_places=1, editable=False)
    
    published = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "stories"
    
    @property
    def is_saved(self):
        if self.saved.exists():
            return True
        return False
            
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
        new_version = self.version + Decimal(0.1)   
        return new_version
            
      
    def save(self, *args, **kwargs):
        if self.pk:
            original_instance = Story.objects.get(pk=self.pk)
            if original_instance.title != self.title:
                self.version = self.small_changes_new_version
            
        super().save(*args, **kwargs)   
    
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
        return f'{self.title} {self.version}'
    


class Text(BaseModel):
    
    story = models.ForeignKey(Story, on_delete=models.CASCADE,  related_name="texts", null=True, blank=True)

    previous_text = models.ForeignKey('Text', on_delete=models.CASCADE,  related_name="choices", blank=True, null=True)
    
    option = models.CharField(max_length=600, null=True, blank=True)
 
    text = models.TextField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            original_instance = Text.objects.get(pk=self.pk)
            
            if original_instance.option != self.option or original_instance.text != self.text:
                self.story.version = self.story.small_changes_new_version
                self.story.save()
            
            if original_instance.previous_text != self.previous_text:  
                if self.story.is_saved:
                    raise TextChangeNotAllowed()

        super().save(*args, **kwargs)
    
    def delete(self, using=None, keep_parents=False):
        if self.story.is_saved:
            raise TextChangeNotAllowed()

        super().delete(using=using, keep_parents=keep_parents)

        
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
    def previous_option(self):
        if self.is_start:
            return "Start"
        else:
            return self.previous_text
    
    
    @property
    def need_duplicate(self):
        if self.story and self.story.published and self.story.is_saved:
            return True
        return False

    

class Saved(BaseModel):
    player = models.ForeignKey(CustomUser, related_name="saved", on_delete=models.CASCADE)
    stage = models.ForeignKey(Text, related_name="saved", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    story =  models.ForeignKey(Story, related_name="saved", on_delete=models.CASCADE)
    
    
    def __str__ (self):
        return f'{self.player} played {self.story.title} (saved)'



    class Meta:
        verbose_name_plural = "Saved"


############ SOCIAL
    
    
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
