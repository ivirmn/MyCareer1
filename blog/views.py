import re

from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags

from django.views.generic import ListView, DetailView
from .models import *

class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'base_article.html'

    def get_object(self, queryset=None):
        # Получаем объект поста или вызываем ошибку 404, если пост скрыт
        return get_object_or_404(Post, slug=self.kwargs['slug'], isPostHidden=False)




class PageListView(ListView):
    model = Page
    template_name = 'home.html'

class PageDetailView(DetailView):
    model = Page
    template_name = 'base_page.html'

    def get_object(self, queryset=None):
        # Получаем объект страницы или вызываем ошибку 404, если страница скрыта
       # return get_object_or_404(Page, slug=self.kwargs['slug'], isPageHidden=False)
        return get_object_or_404(Page, slug=self.kwargs['slug'], )





def tag_posts(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = tag.post_set.all()
    return render(request, 'tag-posts.html', {'tag': tag, 'posts': posts})

def debug_blog(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        text = strip_tags(post.content)
        images = re.findall('src="(.*?)"', post.content)
        tags = post.tags.all()
        tags_list = [tag.name for tag in tags]
        tags_str = ', '.join(tags_list)
        return render(request, 'debug_blog.html', {'text': text, 'images': images, 'tags_str': tags_str})
    return render(request, 'debug_blog.html')