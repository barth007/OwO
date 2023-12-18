from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BlogForm, NewCommentForm
from .models import Blog, Blog_Comment
from django.views.generic import ListView, DetailView, View

# Create your views here.
class Blogs_views(ListView):
    model = Blog
    ''' Displays the blogs
        The ListView itself will take care of fetching the objects and passing them to the
        template, so you don't need to manually fetch and pass the blogs as you did with 
    '''
    contest_object_name = 'blogs'
    template_name = 'blog/blogs.html'
    paginate_by = 4

# @login_required(login_url='/login')

class Blog_details(DetailView):
    model = Blog
    template_name = 'blog/blog_details.html'

    def get_context_data(self, **kwargs):
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
        new_comment = Blog_Comment(
            content=request.POST.get('content'),
            author=self.request.user,
            blog_commented=self.get_object()
        )
        new_comment.save()

        # Use reverse() to get the URL for the Blog_details view
        url = reverse('blog_details', kwargs={'pk': self.get_object().pk})

        return redirect(url)

class Like_Blog(View):
    """ Like counts
    """
    model = Blog

    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)

        if blog.likes.filter(pk=request.user.id).exists():
            blog.likes.remove(request.user.id)
        else:
            blog.likes.add(request.user.id)
            # we have access to the remove and add method because we are using manytomanyfields for like
            blog.save()
            # return HttpResponseRedirect(reverse('blog_details', args=[str(pk)]))
            return redirect('blog_details', pk=pk)

        # Default return statement if the if-else condition is not met
        # return HttpResponseRedirect(reverse('blog_details', args=[str(pk)]))
        return redirect('blog_details', pk=pk)

