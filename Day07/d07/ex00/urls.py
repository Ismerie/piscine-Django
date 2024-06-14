from django.urls import path
from . import views
from .views import Articles, LoginPage, Home, Publications, Detail, Logout, Favourites, Register, Publish

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('articles/', Articles.as_view(), name='articles'),
    path('login/', LoginPage.as_view(), name='login'),
    path('publications/', Publications.as_view(), name='publications'),
    path('detail/<int:pk>/', Detail.as_view(), name='article-detail'),
    path('logout/', Logout.as_view(), name='logout'),
    path('favourites/', Favourites.as_view(), name='favourites'),
    path('register/', Register.as_view(), name='register'),
    path('publish/', Publish.as_view(), name='publish'),
]