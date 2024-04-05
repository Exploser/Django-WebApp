from django.shortcuts import render
from .models import Posts

# Create your views here.

def post_list_and_create(request):
    qs = Posts.objects.all()
    return render(request, 'posts/main.html', {'qs':qs})

