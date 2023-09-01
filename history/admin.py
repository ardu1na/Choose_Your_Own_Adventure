from django.contrib import admin
from history.models import Profile, History, TextHistory, Choices, Genre




class ChoicesInline(admin.TabularInline):
    model= Choices
    extra= 0
    fk_name = "previous_text"
    show_change_link = True

class TextHistoryInline(admin.TabularInline):
    model= TextHistory
    extra= 0
    show_change_link = True

    
class HistoryAdmin(admin.ModelAdmin):
    inlines = TextHistoryInline,
admin.site.register(History, HistoryAdmin)


class TextHistoryAdmin(admin.ModelAdmin):
    inlines = ChoicesInline,
admin.site.register(TextHistory, TextHistoryAdmin)


    
    
    
admin.site.register(Profile)
admin.site.register(Choices)
admin.site.register(Genre)
