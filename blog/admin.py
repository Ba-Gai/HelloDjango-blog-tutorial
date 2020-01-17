from django.contrib import admin

# Register your models here.
from blog.models import Post, Tag, Category

# PostAdmin 来配置 Post 在 admin 后台的一些展现形式。
class PostAdmin(admin.ModelAdmin):
    # list_display 属性控制 Post 列表页展示的字段
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    # fields 属性，用来控制表单展现的字段
    fields = ['title', 'body', 'excerpt', 'category', 'tags']
    # obj.save()。它的作用就是将此 Modeladmin 关联注册的 model 实例（这里 Modeladmin 关联注册的是 Post）保存到数据库。
    # 一个是 request，即此次的 HTTP 请求对象，第二个是 obj，即此次创建的关联对象的实例，
    # 于是通过复写此方法，就可以将 request.user 关联到创建的 Post 实例上，然后将 Post 数据再保存到数据库：
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

# 把新增的PostAdmin也添加进来
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)
