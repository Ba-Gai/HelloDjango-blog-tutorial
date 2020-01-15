from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    # list_display 属性控制 Post 列表页展示的字段
    list_display = ['name', 'email', 'url', 'post', 'created_time']
    # fields 属性，用来控制表单展现的字段
    fields = ['name', 'email', 'url', 'text', 'post']


admin.site.register(Comment, CommentAdmin)
