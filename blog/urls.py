from django.urls import path, include
from .views import Blogs_views, Blog_details, Like_Blog


urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('blogs/', Blogs_views.as_view(), name='blogs'),
    path('blog_details/<int:pk>/', Blog_details.as_view(), name='blog_details'),
    path('blog_details/<int:pk>/like', Like_Blog.as_view(), name='blog_likes'),
    # path('comment/<int:pk>/', blog_comment, name='comment')
]
