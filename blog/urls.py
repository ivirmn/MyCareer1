
from django.urls import include, path

from blog import views
from blog.views import *

urlpatterns = [
    path('p/<slug:slug>/', BlogDetailView.as_view(), name='post_detail'),
    path('tag/<slug:tag_slug>/', tag_posts, name='tag_posts'),
    path('debug_blog/', debug_blog, name='debug_blog'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail')
]