from django.contrib import admin
from history.models import Profile, History, Text, Genre, Like, Saved





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

    
class HistoryInline(admin.TabularInline):
    model= History
    extra= 0
    show_change_link = True
    
class HistoryAdmin(admin.ModelAdmin):
    inlines = TextInline, LikesInline
    list_display = ['title', 'version','author', 'get_likes', 'get_users_who_liked']
admin.site.register(History, HistoryAdmin)


class TextAdmin(admin.ModelAdmin):
    inlines = TextInline,
    list_display = ['history', 'option', 'previous_option']
admin.site.register(Text, TextAdmin)


class ProfileAdmin(admin.ModelAdmin):
    inlines = HistoryInline, LikesInline, SavedInline
admin.site.register(Profile, ProfileAdmin)

    
    
admin.site.register(Genre)
admin.site.register(Like)
admin.site.register(Saved)
