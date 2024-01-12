from django.contrib import admin
from .models import Blog, Blog_Comment

class BlogAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'image', 'content', 'status', 'slug', 'blog_category', 'published_at')
    list_filter = ('status',)
    search_fields = ('content', 'title')
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog_commented', 'content')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Blog_Comment, CommentAdmin)
