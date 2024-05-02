from django.urls import path
from .views import my_profile_view
from .views import login_page

app_name = 'profiles'

urlpatterns = [
    path('my/', my_profile_view, name='my-profile'),
    path('login/', login_page, name='login')
]
