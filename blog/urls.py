from django.urls import path, include
from .views import Blogs_views, Blog_details, Like_Blog, search_blogs


urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('blogs/', Blogs_views.as_view(), name='blogs'),
    path('blog_details/<int:pk>/', Blog_details.as_view(), name='blog_details'),
    path('blog_details/like/<int:pk>/', Like_Blog.as_view(), name='blog_likes'),
    # path('blog_details/<int:pk>/unlike/', Unlike_Blog.as_view(), name='unlike_blog'),
    path('search/', search_blogs, name='search_blogs'),
]
