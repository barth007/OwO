# Generated by Django 4.2.8 on 2023-12-18 08:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_remove_blog_comments_suggestion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(null=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
