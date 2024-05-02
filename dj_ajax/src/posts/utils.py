from .models import Posts
from profiles.models import Profile
from django.http import HttpResponse
from django.shortcuts import redirect

def action_permission(func):
    def wrapper(request, **kwargs):
        pk = kwargs.get('pk')
        profile = Profile.objects.get(user=request.user)
        post = Posts.objects.get(pk=pk)
        if profile.user == post.author.user:
            return func(request, **kwargs)
        else:
            return redirect('post:main-board')
    
    return wrapper