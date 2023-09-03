from decimal import Decimal, ROUND_DOWN
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

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
    
    version = models.DecimalField(default=1, max_digits=4, decimal_places=1)
    
    published = models.BooleanField(default=False)
    
    has_changes = models.BooleanField(default=False)
    has_big_changes = models.BooleanField(default=False)
    
    is_last_version = models.BooleanField(default=True)
    
    @property
    def need_duplicate(self):
        if self.pk and self.published and self.is_saved:
            return True
    
    def save(self, *args, **kwargs):
        if self.need_duplicate:
            
            if self.has_big_changes:
                
                               
                # duplicate instance and related texts and close this.
                
                version = self.version.quantize(Decimal('1.'), rounding=ROUND_DOWN)
                new_version = version + 1
                
                
                new = History.objects.create(
                    author=self.author,
                    about = self.about,
                    genre= self.genre,
                    title = self.title,
                    version = new_version,
                    published=False,
                    
                    )
                texts = self.texts.all()
                new_texts= []
                for text in texts:
                    if text.is_start:
                        previous_text=None
                        option = None
                    else:
                        previous_text=text.previous_text
                        option = text.option
                    new_text = Text(previous_text=previous_text, option=option, text=text.text)
                    new_text.save()
                    new_texts.append(new_text)
                new.texts.set(new_texts)                 
                
                self.has_big_changes = False
                self.published = False 
                self.is_last_version = False
                
            elif self.has_changes:
                self.version += Decimal(0.1)
                self.has_changes = False
                
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
    version = models.DecimalField(default=1, max_digits=4, decimal_places=1)
    # TODO: is current version +  finished into method
    # override last saved 
    
    def save(self, *args, **kwargs):
        self.version = self.stage.history.version
        super().save(*args, **kwargs)
    
    
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
        return self.option if self.option else self.history_title
    
    @property
    def history_title (self):
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
        if self.is_start:
            return "Start"
        else:
            return self.previous_text
    
    
    @property
    def need_duplicate(self):
        if self.history and self.history.published and self.history.is_saved:
            return True
    
    def save(self, *args, **kwargs):
        
        
        if self.pk == None:
        ## is new TESTED OK
            
            # auto asign history when is not the first text
            if self.history == None and self.is_start == False:
                self.history = self.previous_text.history
                
               
            if self.need_duplicate: # duplicate all
                version = self.history.version.quantize(Decimal('1.'), rounding=ROUND_DOWN)
                new_version = version + 1
                
                new = History.objects.create(
                    author=self.history.author,
                    about = self.history.about,
                    genre= self.history.genre,
                    title = self.history.title,
                    version = new_version,
                    published=False
                    
                    )
                self.history.published = False
                self.history.is_last_version = False
                self.history.save()
                texts = Text.objects.filter(history=self.history).exclude(pk=self.pk)
                new_texts= []
                for text in texts:
                    if text.is_start:
                        previous_text=None
                        option = None
                    else:
                        previous_text=text.previous_text
                        option = text.option
                    new_text = Text.objects.create(previous_text=previous_text, option=option, text=text.text)
                    new_texts.append(new_text)
                
                self.history = new 
                new.texts.set(new_texts) 
                # TODO: desde el front se manda a seguir editando el nuevo
            super().save(*args, **kwargs)
        else:
            if self.need_duplicate:
            
                original_instance = self.__class__.objects.get(pk=self.pk)
                if original_instance.previous_text != self.previous_text:
                    
                    version = self.history.version.quantize(Decimal('1.'), rounding=ROUND_DOWN)
                    new_version = version + 1
                    
                    new = History.objects.create(
                        author=original_instance.history.author,
                        about = original_instance.history.about,
                        genre= original_instance.history.genre,
                        title = original_instance.history.title,
                        version = new_version,
                        published=False
                        
                        )
                    old_history = original_instance.history
                    old_history.published = False
                    old_history.is_last_version = False                   
                    
                    old_texts = Text.objects.filter(history=original_instance.history).exclude(pk=self.pk)
                    new_texts= []
                    for text in old_texts:
                        if text.is_start:
                            previous_text=None
                            option = None
                        else:
                            previous_text=text.previous_text
                            option = text.option
                            
                        new_text = Text.objects.create(
                            previous_text=previous_text,
                            option=option,
                            text=text.text
                            )
                        new_texts.append(new_text)
                    
                    self.history = new 
                    super(self).save(*args, **kwargs)
                    old_history.save()
                    new.texts.set(new_texts) 
                    # TODO: desde el front se manda a seguir editando el nuevo
                    new.save()
                    

                    
                else:
                    self.history.has_changes = True
                    super().save(*args, **kwargs)
                    self.history.save()
                
            
        


    
@receiver(pre_delete, sender=Text)
def text_deleted_handler(sender, instance, **kwargs):
    # When a Text instance is deleted, update its associated History's has_big_changes field to True
    if instance.history and instance.history.published and instance.history.is_saved:
        instance.history.has_big_changes = True
        instance.history.save()
        ## TODO: HERE IT SHOULD CHANGE THE NEW VERSION OR ID FOR EACHOTHER BECAUSE IT CREATE A DPLICATE INSTANCE BUT WITH VALUE CHANGED. THE DELETED ONE IS MISS PLACED
