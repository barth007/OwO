from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from django.contrib.auth.models import User


BLOG_CATEGORY = [
    ('finance', 'Finance'),
    ('health', 'Health'),
    ('web_Design', 'Web Design'),
    ('technology', 'Technology'),
    ('banking_services', 'Banking Services'),
    ('investment', 'Investment'),
    ('financial_markets', 'Financial Markets'),
    ('credit_cards', 'Credit Cards'),
    ('mortgages', 'Mortgages'),
    ('online_banking', 'Online Banking'),
    ('personal_finance', 'Personal Finance'),
    ('business_finance', 'Business Finance'),
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
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)
    image = models.ImageField(upload_to='blog_img', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=PUBLISH_STATUS, default='draft', help_text="Select the status of your blog")
    blog_category = models.CharField(max_length=20, choices=BLOG_CATEGORY, default='draft', help_text="Select the category of your blog")
    slug = models.SlugField(max_length=255, unique=True, help_text="Enter a URL-friendly title for your blog", null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    # displayed in the Django admin site
    
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ['-created_at']

    @property
    def number_of_comments(self):
        return BlogComment.objects.filter(blogpost_connected=self).count()
    
    @staticmethod
    def is_published():
        ''' Checks that a blog is published
        '''
        return Blog.objects.filter(status='published').exists()


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
