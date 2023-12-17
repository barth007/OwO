from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from django.contrib.auth.models import User

BLOG_CATEGORY = [
    ('technology', 'Technology'),
    ('finance', 'Finance'),
    ('health', 'Health'),
]

class Blog(models.Model):
    """ Django models for a blog app
    """
    PUBLISH_STATUS = [
            ('draft', 'Draft'),
            ('published', 'Published'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=255, help_text="Enter the title of your blog", verbose_name="Blog Title")
    content = HTMLField(help_text="Write the content of your blog here")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes')
    image = models.ImageField(upload_to='blog_img', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=PUBLISH_STATUS, default='draft', help_text="Select the status of your blog")
    blog_category = models.CharField(max_length=20, choices=BLOG_CATEGORY, default='draft', help_text="Select the category of your blog")
    slug = models.SlugField(max_length=255, unique=True, help_text="Enter a URL-friendly title for your blog")
    published_at = models.DateTimeField(null=True, blank=True)

    '''It also helps with Search Engine Optimization (SEO), which means it makes it easier for search engines
    like Bing to find your blog post when people search for topics related to your post.
    '''
    # can be omitted
    title_suggestion = models.TextField(null=True, blank=True, help_text="Suggestions for improving the title")
    content_suggestion = models.TextField(null=True, blank=True, help_text="Suggestions for improving the content")
    comments_suggestion = models.TextField(null=True, blank=True, help_text="Suggestions for managing comments")

    # displayed in the Django admin site
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ['-created_at']
        permissions = [
            ("can_create_post", "Can create a new blog post"),
            ("can_edit_post", "Can edit a blog post"),
            ("can_delete_post", "Can delete a blog post"),
            ("can_view_post", "Can view a blog post"),
        ]

    @property
    def number_of_comments(self):
        return BlogComment.objects.filter(blogpost_connected=self).count()

    def is_published(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        supper.save(*args, *kwargs)

    def __str__(self) -> str:
        return f"{self.title} by {self.author.username}"

class Blog_Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments')
    blog_commented = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField(help_text="Write your comment here")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']


    def __str__(self) -> str:
        return f"Comment by {self.author.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
