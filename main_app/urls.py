from django.urls import path
from . import views
from .views import Home, Signup, ProfileView, PostDetail, UpdateProfile, CitiesView, PostCreate, PostUpdate, MainUserCity, PostDelete, ProfileViewOther, AboutView, CommentCreate

urlpatterns = [
	path('', Home.as_view(), name="home"),
    path('accounts/signup/', Signup.as_view(), name="signup"),
    path('accounts/profile/', ProfileView.as_view(), name="profile_view"),
    path('posts/<int:pk>/', PostDetail.as_view(), name="post_detail"),
    path('posts/new/', PostCreate.as_view(), name="post_create"),
    path('posts/<int:pk>/edit/', PostUpdate.as_view(), name="post_update"),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name="post_delete"),
    path('accounts/profile/update/', UpdateProfile.as_view(), name="update_profile"),
    path('accounts/profile/<int:pk>/', ProfileViewOther.as_view(), name="profile_view_other"), 
    path('cities/<int:pk>/', CitiesView.as_view(), name="cities_view"),
    path('cities/', MainUserCity.as_view(), name="user_city"),
    path('about/', AboutView.as_view(), name='about_view'),
    path('posts/<int:pk>/comments/new/', CommentCreate.as_view(), name="comment_create"),
    
]