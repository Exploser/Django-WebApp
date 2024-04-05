from django.shortcuts import render
from .models import Posts
from django.http import JsonResponse

# Create your views here.

def post_list_and_create(request):
    qs = Posts.objects.all()
    return render(request, 'posts/main.html', {'qs':qs})


def hello_world_view(request):
    return JsonResponse({'text': 'HELLO WORLD'})