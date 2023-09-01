from django.contrib import admin
from history.models import Profile, History, TextHistory, Choice, Genre, Like, Saved




class ChoiceInline(admin.TabularInline):
    model= Choice
    extra= 0
    fk_name = "previous_text"
    show_change_link = True

class TextHistoryInline(admin.TabularInline):
    model= TextHistory
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

class SavedInline(admin.TabularInline):
    model= Saved
    extra= 0
    show_change_link = True
    
    
    
class HistoryInline(admin.TabularInline):
    model= History
    extra= 0
    show_change_link = True
    
class HistoryAdmin(admin.ModelAdmin):
    inlines = TextHistoryInline, LikesInline
admin.site.register(History, HistoryAdmin)


class TextHistoryAdmin(admin.ModelAdmin):
    inlines = ChoiceInline,
admin.site.register(TextHistory, TextHistoryAdmin)


class ProfileAdmin(admin.ModelAdmin):
    inlines = HistoryInline, LikesInline, SavedInline
admin.site.register(Profile, ProfileAdmin)


    
    
admin.site.register(Choice)
admin.site.register(Genre)
admin.site.register(Like)
admin.site.register(Saved)
