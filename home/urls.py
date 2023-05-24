from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('relevant', views.relevant, name='relevant'),
    path('search', views.search, name='search'),
    path('signup', views.signup, name='signup'),
    path('login', views.handle_login, name='handle_login'),
    path('logout', views.handle_logout, name='handle_logout'),
]
