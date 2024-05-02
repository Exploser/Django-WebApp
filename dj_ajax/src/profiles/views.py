from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.

@login_required
def my_profile_view(request):
    obj = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=obj)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if form.is_valid():
            instance = form.save()
            return JsonResponse({
                'bio': instance.bio,
                'avatar': instance.avatar.url if instance.avatar else None,
                'user': instance.user.username
            })
    context = {
        'obj': obj,
        'form': form,
    }

    return render(request, 'profiles/main.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page after successful login
        else:
            # Return an error message perhaps
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'profiles/login.html')