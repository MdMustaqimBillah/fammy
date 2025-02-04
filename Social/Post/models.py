from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='user_post')
    image = models.ImageField(upload_to='post_pics/', blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    posted = models.DateTimeField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted']
    

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='user_comment')
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='post_comment')
    comment = models.TextField(blank=True, null=True)
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-posted']


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='post_like')


class CommentReaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='user_comment_reaction')
    comment = models.ForeignKey(Comment, on_delete= models.CASCADE, related_name='comment_reaction')
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='post_comments_reaction')