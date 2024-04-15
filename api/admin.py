from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'by', 'type', 'time', 'score')  
    list_filter = ('type', 'time')  
    search_fields = ('title', 'text', 'by') 
    date_hierarchy = 'time'  
    ordering = ('-time',)  

    fieldsets = (
        (None, {
            'fields': ('title', 'by', 'type', 'text')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('score', 'time', 'parent'),
        }),
    )

admin.site.register(Post, PostAdmin)