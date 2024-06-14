from django.urls import path
from .views.home import home
from .views.signin import signin
from .views.signup import signup
from .views.logout import logout_view
from .views.tip import like_tip, dislike_tip, delete

urlpatterns = [
    path('', home, name='home'),
    path('signin/', signin , name='signin'),
    path('signup/', signup , name='signup'),
    path('logout/', logout_view , name='logout_view'),
    path('like/', like_tip , name='like_tip'),
    path('dislike/', dislike_tip , name='dislike_tip'),
    path('delete/', delete , name='delete'),
]