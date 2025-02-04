from django.forms import BaseModelForm
from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from Authentication import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,DeleteView
from . import models
from django.utils import timezone
from django.contrib import messages
from Post.models import Post



# Create your views here.


def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Post:home'))
    else:
        form = forms.SignUpForm()
        if request.method == 'POST':
            form = forms.SignUpForm(request.POST)
            if form.is_valid():
                user =form.save()
                user_profile = models.UserProfile()
                user_profile.user = user
                user_profile.first_name = form.cleaned_data.get('first_name')
                user_profile.last_name = form.cleaned_data.get('last_name')
                user_profile.save()
                messages.success(request,'Account Created Successfully')
                return HttpResponseRedirect(reverse('user_login'))
            else:
                messages.error(request,'Invalid data')
    dictionary = {
        'form': form,
    }
    return render(request, 'Authentication/sign_up.html', context= dictionary)



def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Post:home'))
    else:

        form = forms.LoginForm()
        if request.method == 'POST':
            form = forms.LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('Post:home'))
            else:
                messages.error(request,'Invalid username or password')
    dictionary = {
        'form': form,
     }
    return render(request, 'Authentication/log_in.html', context=dictionary)


@login_required
def update_profile(request):
    try:
         current_user = models.UserProfile.objects.get(user=request.user)

    except models.UserProfile.DoesNotExist:
        current_user = models.UserProfile(user=request.user, dob= timezone.now())
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated successfully')
            return HttpResponseRedirect(reverse('Authentication:profile'))
    else:
       form = forms.UserProfileForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'Authentication/user_details_form.html', context=context)

@login_required
def profile(request):
        user = request.user

        posts = Post.objects.filter(user=user)

        dictionary = {
        'user':request.user,
        'posts':posts
        }
        return render(request, 'Authentication/user_profile.html', context=dictionary)


@login_required
def password_change(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user= form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Password changed successfully')            
            return HttpResponseRedirect(reverse('Post:home'))
    dictionary = {
        'form': form,
    }
    return render(request, 'Authentication/password_change.html',context=dictionary)


@login_required
def follow(request,pk):
    user = models.User.objects.get(pk=pk)
    follower = request.user
    already_followed = models.Following.objects.filter(follower = follower, user=user).exists()

    if already_followed == False:
        follow = models.Following(follower=follower, user=user)
        follow.save()
    return HttpResponseRedirect(reverse('Authentication:author_profile', kwargs={'pk': pk}))


@login_required
def unfollow(request,pk):
    user = models.User.objects.get(pk=pk)
    follower = request.user
    already_followed = models.Following.objects.filter(follower=follower, user=user).exists()
    
    if already_followed == True:
        already_followed = models.Following.objects.filter(follower=follower, user=user)
        already_followed.delete()
    return HttpResponseRedirect(reverse('Authentication:author_profile', kwargs={'pk': pk}))



@login_required
def author_profile(request,pk):
    user = models.User.objects.get(pk=pk)
    follower = request.user
    followed = models.Following.objects.filter(user=user,follower=follower)
    dictionary = {
        'author':user,
        'followed':followed
    }
    return render(request, 'Authentication/author_profile.html', context=dictionary)


class AccountDelete(LoginRequiredMixin,DeleteView):
    model = models.User
    template_name = 'Authentication/account_delete.html'
    success_url = '/'
