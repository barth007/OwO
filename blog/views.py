from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import NewCommentForm
from .models import Blog, Blog_Comment
from django.http import JsonResponse
from .utils import ImageSizeValidationMixin
from django.views.generic import ListView, DetailView, View, RedirectView


# Create your views here.
class Blogs_views(ImageSizeValidationMixin, ListView):
    ''' Displays the blogs
    '''
    model = Blog

    context_object_name = 'blogs'
    template_name = 'blog/blog.html'
    paginate_by = 4

    def get_queryset(self):
        ''' Overrides the original queryset
        '''
        queryset = super().get_queryset()
        queryset = queryset.filter(status='published')
        return queryset


class Blog_details(DetailView):
    '''Handles a single blog details'''
    model = Blog
    template_name = 'blog/blog_details.html'

    def get_context_data(self, **kwargs):
        ''' Simply a method that can be used to pass additional
            information to the template.
        '''
        data = super().get_context_data(**kwargs)

        # Check if the user has liked the blog post
        data['liked_by_user'] = False
        if self.request.user.is_authenticated:
            if self.object.likes.filter(pk=self.request.user.id).exists():
                data['liked_by_user'] = True

        # Retrieve and include comments related to the blog post
        blog_commented = Blog_Comment.objects.filter(
            blog_commented=self.object).order_by('-created_at')
        data['comments'] = blog_commented

        # Include a comment form for a user
        data['comment_form'] = NewCommentForm()
        
        data['related_content'] = Blog.objects.filter(blog_category=self.object.blog_category).order_by('blog_category')
        return data


    def post(self, request, *args, **kwargs):
        ''' create a new comment
        '''
        content = request.POST.get('content')
        new_comment = Blog_Comment(
        content=content,
        author=self.request.user,
        blog_commented=self.get_object()
        )
        new_comment.save()
        # Create a dictionary containing the new comment data
        new_comment_data = {
            'content': new_comment.content,
            'author': new_comment.author.username,
            'created_at': new_comment.created_at,
        }

        # Return a JSON response with the new comment data
        return JsonResponse(new_comment_data)


class Like_Blog(View):
    model = Blog

    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)

        if blog.likes.filter(pk=request.user.id).exists():
            blog.likes.remove(request.user.id)
        else:
            blog.likes.add(request.user.id)
            blog.save()

        # Create a JSON response with the updated like count
        response_data = {
            'likes_count': blog.likes.count(),
        }
        return JsonResponse(response_data)


def search_blogs(request):
    ''' Search for a blog in the database
        query parameters: title and content
    '''
    query = request.GET.get('q')

    if query:
        results = Blog.objects.filter(
            Q(slug__icontains=query) | Q(content__icontains=query)
        ).distinct()
    else:
        results = Blog.objects.all()

    context = {
        'results': results,
        'query': query
    }
    return render(request, 'blog/search_results.html', context)

class Category(ListView):
    model = Blog
    template_name = 'blog/category.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        """Query for blog posts in the specified category"""
        val = self.kwargs.get('val')
        blogs = Blog.objects.filter(blog_category=val)
        return blogs
