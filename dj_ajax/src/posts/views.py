from django.shortcuts import render
from .models import Posts
from django.http import JsonResponse

# Create your views here.

def post_list_and_create(request):
    qs = Posts.objects.all()
    return render(request, 'posts/main.html', {'qs':qs})

def load_post_data_view(request):
    qs = Posts.objects.all()
    data = []
    for obj in qs:
        item = {
            'id': obj.id,
            'title': obj.title,
            'body': obj.body,
            'author': obj.author.user.username
        }
        data.append(item)
    return JsonResponse({'data':data})


def hello_world_view(request):
    return JsonResponse({'text': 'HELLO WORLD'})