from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import BlogForm, NewCommentForm
from .models import Blog, Blog_Comment
from django.views.generic import ListView, DetailView, View, RedirectView
from django.http import JsonResponse
from .utils import check_image_size

# Create your views here.
class Blogs_views(ListView):
    ''' Displays the blogs
        The ListView itself will take care of fetching
            the objects and passing them to the
        template, so you don't need to manually fetch
            and pass the blogs as you did with 
    '''
    model = Blog

    contest_object_name = 'blogs'
    template_name = 'blog/blogs.html'
    paginate_by = 3

    def get_queryset(self):
        ''' overides the original queryset in the class
        '''
        img_width = 1200
        img_height = 600

        for blog in super().get_queryset():
            if blog.image:
                check_image_size(blog.image.path, img_width, img_height)
        return super().get_queryset()


# @login_required()
class Blog_details(DetailView):
    '''Handles the blog detail page'''
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
        # Include a comment form for authenticated users
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm()

        return data
        
    def post(self, request, *args, **kwargs):
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

    def get_queryset(self):
        ''' overides the original queryset in the class
        '''
        img_width = 1200
        img_height = 600

        for blog in super().get_queryset():
            if blog.image:
                check_image_size(blog.image.path, img_width, img_height)
        return super().get_queryset()


# @login_required
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

        return JsonResponse(response_data, safe=False)


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
    template_name = 'blog/category2.html'
    context_object_name = 'blogs'
    paginate_by = 3

    def get_queryset(self):
        """Query for blog posts in the specified category"""
        val = self.kwargs.get('val')
        blogs = Blog.objects.filter(blog_category=val)
        
        img_width = 1200
        img_height = 600

        for blog in blogs:
            if blog.image:
                check_image_size(blog.image.path, img_width, img_height)

        return blogs
