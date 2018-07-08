from django.contrib import admin
from .models import PostModel, Comment
class CommentInline(admin.TabularInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
admin.site.register(PostModel, PostAdmin)
