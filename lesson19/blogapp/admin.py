import datetime

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Posts


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'content_str', 'link']
    search_fields = ['title', 'author']

    ordering = ['-created']
    list_filter = ['author']

    fieldsets = (
        ('Заголовок, содержимое', {'fields': ['title', 'content']}),
        ('Автор, дата создания', {'fields': ['author', 'created']}),
    )

    actions = ['update_created']

    @admin.display(description='content')
    def content_str(self, post: Posts):
        return mark_safe(f"""
        <div style="color: green;" > {post.content[:30]} ... </div>   
        """)

    @admin.display(description='link')
    def link(self, post: Posts):
        return mark_safe(f'<a href="/post/{ post.id }"> Открыть </a>')

    @admin.action(description='Обновить дату создания')
    def update_created(self, request, queryset):
        queryset.update(created=datetime.datetime.now())
