from django.shortcuts import render
from .models import Posts
from django.http import JsonResponse, HttpResponse
from .forms import PostForm
from profiles.models import Profile
from posts.models import Photo
from django.shortcuts import get_object_or_404
from .utils import action_permission
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.
def post_list_and_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if form.is_valid() and request.user.is_authenticated:
                author_profile, created = Profile.objects.get_or_create(user=request.user)
                instance = form.save(commit=False)
                instance.author = author_profile
                instance.save()
                return JsonResponse({
                    'title': instance.title,
                    'body': instance.body,
                    'author': instance.author.user.username,
                    'id': instance.id})
            else:
                return JsonResponse({'error': 'Invalid form data or user not authenticated'}, status=400)
    else:
        form = PostForm()
    return render(request, 'posts/main.html', {'form': form})


def post_detail(request, pk):
    obj = get_object_or_404(Posts, pk=pk)
    form = PostForm()

    context = {
        'obj': obj,
        'form': form,
    }

    return render(request, 'posts/detail.html', context)

def load_post_data_view(request, num_posts):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        visible = 3
        upper = num_posts
        lower = upper - visible
        size = Posts.objects.all().count()
        qs = Posts.objects.all()
        data = []
        for obj in qs:
            item = {
                'id': obj.id,
                'title': obj.title,
                'body': obj.body,
                'liked': True if request.user in obj.liked.all() else False,
                'count': obj.like_count,
                'author': obj.author.user.username
            }
            data.append(item)
        return JsonResponse({'data':data[lower:upper], 'size': size})
    else:
        return redirect('post:main-board')
    
def post_detail_data_view(request, pk):
    obj = Posts.objects.get(pk=pk)
    data = {
        'id': obj.id,
        'title': obj.title,
        'body': obj.body,
        'author': obj.author.user.username,
        'logged_in': request.user.username,
    }
    return JsonResponse({'data': data})


def like_unlike_post(request):
    # if request.is_ajax():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            pk = request.POST.get('pk')
            obj = get_object_or_404(Posts, pk=pk)
            if request.user.is_authenticated:  # Check if user is authenticated
                if request.user in obj.liked.all():
                    liked = False
                    obj.liked.remove(request.user)
                else:
                    liked = True
                    obj.liked.add(request.user)
                return JsonResponse({'liked': liked, 'count': obj.like_count})
            else:
                return JsonResponse({'error': 'User not authenticated'})
        else:
            return JsonResponse({'error': 'Invalid request method'})
    else:
        return redirect('post:main-board')

@action_permission
@login_required
def update_post(request, pk):
    obj = Posts.objects.get(pk = pk)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        new_title = request.POST.get('title')
        new_body = request.POST.get('body')
        obj.title = new_title
        obj.body = new_body
        obj.save()
        return JsonResponse ({
            'title': new_title,
            'body': new_body,
        })
    return redirect('post:main-board')
    

@action_permission
@login_required
def delete_post(request, pk):
    obj = Posts.objects.get(pk = pk)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        obj.delete()
        return JsonResponse({})
    return JsonResponse({'msg' : 'Your are not authorized to do that'})

def image_upload_view(request):
    if request.method == 'POST':
        img = request.FILES.get('file')
        new_post_id = request.POST.get('new_post_id')
        post = Posts.objects.get(id=new_post_id)
        Photo.objects.create(image=img, post=post)
        return HttpResponse()
    else:
        return redirect('post:main-board')
