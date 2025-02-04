from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from . import models
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.views.generic.list import ListView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect,get_object_or_404
from django.urls import reverse, reverse_lazy
from Authentication.models import Following,User,UserProfile
from .forms import CommentForm
from django.contrib import messages
from django.db.models import Q


# Create your views here.
@login_required
def post_like_info(request,user, posts):
    liked_info = models.Like.objects.filter(user=user, post__in=posts).values_list('post_id', flat=True)
    return list(liked_info)




@login_required
def home(request, pk=None):

    search = False
    result = None

    if request.method =='GET':
        search= request.GET.get('search','')
        if search:
            profiles= UserProfile.objects.filter(
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search)
                ).select_related('user')
            result = [profile.user for profile in profiles]
        else:
            resule = None
        
    
    user = request.user
    following_users = Following.objects.filter(follower=user).values_list('user',flat=True)
    following_posts = models.Post.objects.filter(user__in=following_users)
    liked_info = post_like_info(request,user=user, posts=following_posts)
    liked = {post.id:post.id in liked_info for post in following_posts}
           
        

    dictionary = {
        
        'following_posts': following_posts,
        'liked':liked,
        'search':search,
        'result':result
    
    }

    return render(request, 'Post/home.html', context=dictionary)



class PostMaking(LoginRequiredMixin, CreateView):
    model = models.Post
    fields = ['image','caption']
    template_name = 'Post/post.html'

    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False) 
            post.user = self.request.user
            post.save()
            messages.success(self.request,'Post created successfully')
            return HttpResponseRedirect(reverse('Post:home'))
        
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = models.Post
    fields = ['image','caption']
    template_name = 'Post/post_update.html'

    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False) 
            post.user = self.request.user
            post.save()
            messages.success(self.request,'Post updated successfully')
            return HttpResponseRedirect(reverse('Post:home'))
        

class PostDelete(LoginRequiredMixin, DeleteView):
    model = models.Post
    template_name = 'Post/post_delete.html'
    success_url ='/Post/'



class Commenting(LoginRequiredMixin,CreateView):
    model = models.Comment
    fields = ['comment']
    template_name = 'Post/comment.html'

    def form_valid(self, form):
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.user = self.request.user
            comment.post = models.Post.objects.get(pk=self.kwargs['pk'])
            comment.save()
            return HttpResponseRedirect(reverse('Post:home'))
        
class UpdateComment(LoginRequiredMixin,UpdateView):
    model = models.Comment
    fields = ['comment']
    template_name = 'Post/comment_update.html'

    def form_valid(self, form):
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.user = self.request.user
            comment.post = models.Post.objects.get(pk=self.kwargs['pk'])
            comment.save()
            return HttpResponseRedirect(reverse('Post:home'))
        

class DeleteComment(LoginRequiredMixin,DeleteView):
    model = models.Comment
    template_name = 'Post/comment_delete.html'
    success_url = ''

@login_required
def liked(request,pk):
    post = models.Post.objects.get(pk=pk)
    user = request.user
    
    liked = models.Like.objects.filter(user=user, post=post).exists()

    if not liked:
        liked = models.Like(user=user, post=post)
        liked.save()
    return HttpResponseRedirect(reverse('Post:home_like',kwargs={'pk':pk}))
   

@login_required  
def undo_like(request, pk):
    post = models.Post.objects.get(pk=pk)
    user = request.user
    liked = models.Like.objects.filter(user=user, post=post).exists()

    if liked:
        liked = models.Like.objects.get(user=user, post=post)
        liked.delete()
    return HttpResponseRedirect(reverse('Post:home_like',kwargs={'pk':pk}))


def get_comment_reactions(user, post, comments):
    comment_reactions = models.CommentReaction.objects.filter(
        user=user, post=post, comment__in=comments
    ).values_list('comment__id', flat=True)
    return list(comment_reactions)


@login_required
def comment_on_post(request,pk):
    user = request.user
    form = CommentForm()
    post = models.Post.objects.get(pk=pk)
    comments = post.post_comment.all()
    liked = models.Like.objects.filter(user=user, post=post)
    comment_reactions = get_comment_reactions(user=user, post=post, comments=comments)

    reacted = {comment.id:comment.id in comment_reactions for comment in comments}

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.user = user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('Post:comment',kwargs={'pk':post.pk}))
    dictionary ={
        'post':post,
        'form':form,
        'comments':comments,
        'liked':liked,
        'reacted':reacted
    }
    return render(request, 'Post/comment.html', context=dictionary)






class CommentEdit(LoginRequiredMixin,UpdateView):
    model = models.Comment
    fields = ['comment']
    template_name = 'Post/comment_update.html'

    def form_valid(self, form):
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.user = self.request.user
            comment_obj = models.Comment.objects.select_related('post').get(pk=self.kwargs['pk'])
            post= comment_obj.post
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('Post:comment',kwargs={'pk':post.pk}))
        

class CommentDelete(LoginRequiredMixin,DeleteView):
    model = models.Comment
    template_name = 'Post/comment_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('Post:comment', kwargs={'pk': self.object.post.pk})

@login_required
def inside_liked(request,pk):
    post = models.Post.objects.get(pk=pk)
    user = request.user
    
    liked = models.Like.objects.filter(user=user, post=post).exists()

    if not liked:
        liked = models.Like(user=user, post=post)
        liked.save()
    return HttpResponseRedirect(reverse('Post:comment',kwargs={'pk':pk}))
   

@login_required
def undo_inside_like(request, pk):
    post = models.Post.objects.get(pk=pk)
    user = request.user
    liked = models.Like.objects.filter(user=user, post=post).exists()

    if liked:
        liked = models.Like.objects.get(user=user, post=post)
        liked.delete()
    return HttpResponseRedirect(reverse('Post:comment',kwargs={'pk':pk}))

@login_required
def comment_reaction(request,pk):
    comment = models.Comment.objects.get(pk=pk)
    user = request.user
    post = comment.post
    reacted = models.CommentReaction.objects.filter(user=user, comment=comment, post=post).exists()

    if not reacted:
        reacted = models.CommentReaction(user=user, comment=comment,post=post)
        reacted.save()
    else:
        reacted = models.CommentReaction(user=user, comment=comment, post=post)
        reacted.delete()
    return HttpResponseRedirect(reverse('Post:comment',kwargs={'pk':post.pk}))


@login_required
def undo_comment_reaction(request, pk):
    comment = models.Comment.objects.get(pk=pk)
    user = request.user
    post = comment.post
    reacted = models.CommentReaction.objects.filter(user=user, comment=comment, post=post).exists()

    if reacted:
        reacted = models.CommentReaction.objects.filter(user=user, comment=comment, post=post)
        reacted.delete()
    return HttpResponseRedirect(reverse('Post:comment',kwargs={'pk':post.pk}))



def get_post_reactions(user, posts):
    post_reactions = models.Like.objects.filter(
        user=user, post__in=posts
    ).values_list('post__id', flat=True)
    return list(post_reactions)

@login_required
def my_posts(request):
    user = request.user
    posts = models.Post.objects.filter(user=user)
    post_reactions = get_post_reactions(user=user, posts=posts)
    reacted = {post.id:post.id in post_reactions for post in posts}
    dictionary ={
        'posts':posts,
        'reacted':reacted
    }
    return render(request, 'Post/my_posts.html', context=dictionary)


@login_required
def my_post_like(request,pk):
    post = models.Post.objects.get(pk=pk)
    user = request.user
    
    liked = models.Like.objects.filter(user=user, post=post).exists()

    if not liked:
        liked = models.Like(user=user, post=post)
        liked.save()
    return HttpResponseRedirect(reverse('Post:my_posts'))

@login_required
def undo_my_post_like(request,pk):
    post = models.Post.objects.get(pk=pk)
    user = request.user
    liked = models.Like.objects.filter(user=user, post=post).exists()

    if liked:
        liked = models.Like.objects.get(user=user, post=post)
        liked.delete()
    return HttpResponseRedirect(reverse('Post:my_posts'))


@login_required
def author_posts(request, pk):
    author = models.User.objects.get(pk=pk)
    posts = models.Post.objects.filter(user=author)
    post_reactions = get_post_reactions(user=request.user, posts=posts)
    reacted = {post.id:post.id in post_reactions for post in posts}
    dictionary ={
        'posts':posts,
        'author':author,
       'reacted':reacted
    }
    return render(request, 'Post/author_posts.html', context=dictionary)
