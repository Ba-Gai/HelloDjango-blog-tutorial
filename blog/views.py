import re

from django.shortcuts import render, get_object_or_404
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
# Create your views here.
from django.http import HttpResponse

from .models import Post


# 返回文章列表到'blog/index.html'
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 根据归档时间返回文章列表
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    '''
    这样我们在模板中显示 {{ post.body }} 的时候，就不再是原始的 Markdown 文本了，而是解析过后的 HTML 文本。
    注意这里我们给 markdown 解析函数传递了额外的参数 extensions，它是对 Markdown 语法的拓展，这里使用了三个拓展，
    分别是 extra、codehilite、toc。extra 本身包含很多基础拓展，而 codehilite 是语法高亮拓展，这为后面的实现代码高亮功能提供基础，
    而 toc 则允许自动生成目录（在以后会介绍）。
    '''
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})
