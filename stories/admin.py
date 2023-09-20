from django.contrib import admin
from stories.models import  Story, Text, \
    Genre, Like, Saved, Comment, Rate, Choice




class ChoiceInline(admin.TabularInline):
    model= Choice
    extra= 0
    show_change_link = True
    fk_name = "prev_text"
    
    
class TextInline(admin.TabularInline):
    model= Text
    extra= 0
    show_change_link = True

class SavedInline(admin.TabularInline):
    model= Saved
    extra= 0
    show_change_link = True

class LikesInline(admin.TabularInline):
    model= Like
    extra= 0
    show_change_link = True
    
class CommentInline(admin.TabularInline):
    model= Comment
    extra= 0
    show_change_link = True
    
    
class RateInline(admin.TabularInline):
    model= Rate
    extra= 0
    show_change_link = True
    
class StoryInline(admin.TabularInline):
    model= Story
    extra= 0
    show_change_link = True
    
class StoryAdmin(admin.ModelAdmin):
    inlines = TextInline, LikesInline, CommentInline, RateInline
    list_display = ['title', 'version','author','is_saved', 'likes_q']
    
    def save_model(self, request, obj, form, change):
        if obj.author == None:
            obj.author = request.user
        obj.save()
        
admin.site.register(Story, StoryAdmin)


class TextAdmin(admin.ModelAdmin):
    inlines=[ChoiceInline,]
    list_display = ['story', 'text_data']
admin.site.register(Text, TextAdmin)


admin.site.register(Choice)


    
admin.site.register(Comment)
admin.site.register(Rate)

admin.site.register(Genre)
admin.site.register(Like)
admin.site.register(Saved)
