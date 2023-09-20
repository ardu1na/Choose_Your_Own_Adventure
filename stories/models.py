from decimal import Decimal, ROUND_DOWN
from django.db import models
from rest_framework import exceptions

from users.models import CustomUser

######## UTILS
class TextChangeNotAllowed(exceptions.APIException):
    status_code = 400
    default_detail = "Cannot change this text because the story is already being played by users. Go to api/stories/ < story__id > /clone/ to start a new one from this."
    default_code = "text_change_not_allowed"
    
    
class NewStartTextNotAllowed(exceptions.APIException):
    status_code = 400
    default_detail = "Cannot add another first text because the story already has one. Add a 'before_text'."
    default_code = "text_creation_not_allowed"
    

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
    """
        # TODO:
            - ONLY ONE VERSION CAN BE PUBLISHED
    """
    title = models.CharField(max_length=150)
    about = models.CharField(max_length=800, blank=True, null= True)

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="stories")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  related_name="stories", editable=False, blank=True,  null=True)
    
    version = models.DecimalField(default=1, max_digits=4, decimal_places=2, editable=False)
    
    published = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "stories"
        
    @property
    def created_at(self):
        return f"{self.date_created.strftime('%d-%m-%Y %H:%M')}"
    @property
    def updated_at(self):
        return f"{self.date_updated.strftime('%d-%m-%Y %H:%M')}"
    
    def clone_story(self):
        """
            if user wants to make a big change of an story, and the story is saved by another player,
            he can clone the story with a new version and make the changes there.
            the original story goes to unpublished
            
            an alert must to be show, a message to players, with something like "your playing and old version of this story"
        """
        # Clone the story
        self.published = False
        self.save()
        
        cloned_story = Story(
            title=f"Clon of {self.title}",
            about=self.about,
            genre=self.genre,
            author= self.author,
            version=self.big_changes_new_version, 
            published=False,  
        )
        cloned_story.save()

        text_mapping = {}

        for original_text in self.texts.all():
            cloned_text = Text(
                story=cloned_story,
                option=original_text.option,
                text=original_text.text,
            )
            if original_text.previous_text:
                cloned_text.previous_text = text_mapping.get(original_text.previous_text)
            cloned_text.save()
            text_mapping[original_text] = cloned_text

        return cloned_story
    
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
    def likes_q(self):
        likes = self.likes.all()
        return likes.count()
    
    @property
    def likes_users(self):
        users = CustomUser.objects.filter(likes__story=self)
        if users.exists():
            return users
        else:
            return None
        
        

    def __str__ (self):
        return f'{self.title} {self.version}'
    

class Text(BaseModel):
    
    story = models.ForeignKey(Story, on_delete=models.CASCADE,  related_name="texts", null=True, blank=True)
  
 
    text = models.TextField(null=True, blank=True)
    
    """def save(self, *args, **kwargs):
        if self.pk:
            original_instance = Text.objects.get(pk=self.pk)
            
            if original_instance.option != self.option or original_instance.text != self.text:
                self.story.version = self.story.small_changes_new_version
                self.story.save()
            
            if original_instance.previous_text != self.previous_text:  
                if self.story.is_saved:
                    raise TextChangeNotAllowed()
        else:
            
            if self.previous_text != None:
                self.story = self.previous_text.story
            else:
                story_texts = Text.objects.filter(story=self.story, previous_text=None)
                if story_texts.exists():
                    raise NewStartTextNotAllowed()

        super().save(*args, **kwargs)"""
    
    def delete(self, using=None, keep_parents=False):
        if self.story.is_saved:
            raise TextChangeNotAllowed()

        super().delete(using=using, keep_parents=keep_parents)

    @property  
    def text_data (self):
        text = self.text[:55]
        return text
    
    def __str__ (self):
        return f'{self.text_data} - story {self.story}'
    
    @property
    def story_title (self):
        return self.story.title
    
            
    
    @property
    def need_duplicate(self):
        if self.story and self.story.published and self.story.is_saved:
            return True
        return False

    
class Choice(BaseModel):
    option = models.CharField(max_length=600, null=True, blank=True)
    prev_text = models.ForeignKey(Text, on_delete=models.CASCADE,  related_name="causes", blank=True, null=True)
    next_text = models.ForeignKey(Text, on_delete=models.CASCADE,  related_name="choices", blank=True, null=True)

    
    def __str__(self):
        return self.option
    
class Saved(BaseModel):
    player = models.ForeignKey(CustomUser, related_name="saved", on_delete=models.CASCADE)
    stage = models.ForeignKey(Text, related_name="saved", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    story =  models.ForeignKey(Story, related_name="saved", on_delete=models.CASCADE)
    story_version = models.DecimalField(editable=False, max_digits=4, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.story_version = self.story.version
        super().save(*args, **kwargs)
        
    def __str__ (self):
        return f'{self.player} played {self.story.title} (saved)'



    class Meta:
        verbose_name_plural = "Saved"
        unique_together = ['player', 'story']


############ SOCIAL
    
    
class Like(models.Model):
    user = models.ForeignKey(CustomUser, related_name="likes", on_delete=models.CASCADE, editable=False)
    story = models.ForeignKey(Story, related_name="likes", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def datetime(self):
        return f"{self.date_created.strftime('%d-%m-%Y %H:%M')}"
    def __str__ (self):
        return f'{self.user} liked {self.story.title}'


    class Meta:
        unique_together = ['user', 'story']
    
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
        return f'{self.user.username} rated {self.story.title}'
    class Meta:
        unique_together = ['user', 'story']

    
class Comment(BaseModel):
    comment = models.TextField()
    user = models.ForeignKey(CustomUser, related_name="comments", on_delete=models.CASCADE)
    story = models.ForeignKey(Story, related_name="comments", on_delete=models.CASCADE)
    def __str__ (self):
        return f'{self.user.username} commeted {self.story.title}'

    @property
    def created_at(self):
        return f"{self.date_created.strftime('%d-%m-%Y %H:%M')}"
    @property
    def updated_at(self):
        return f"{self.date_updated.strftime('%d-%m-%Y %H:%M')}"