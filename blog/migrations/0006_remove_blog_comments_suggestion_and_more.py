# Generated by Django 4.2.8 on 2023-12-18 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blog_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='comments_suggestion',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='content_suggestion',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='title_suggestion',
        ),
    ]