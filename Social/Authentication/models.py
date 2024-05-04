from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=200)
    dob = models.DateTimeField(blank=True, null=True)
    choose =(('Male','Male'),('Female','Female'))
    gender = models.CharField(max_length=6,choices=choose)
    location = models.CharField(max_length=100, blank=True, null=True)



class Following(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'follower')
    