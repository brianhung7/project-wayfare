from django.urls import path
from . import views
from .views import Home, Signup, ProfileView, PostDetail, UpdateProfile, CitiesView, PostCreate


urlpatterns = [
	path('', Home.as_view(), name="home"),
    path('accounts/signup/', Signup.as_view(), name="signup"),
    path('accounts/profile/', ProfileView.as_view(), name="profile_view"),
    path('posts/<int:pk>/', PostDetail.as_view(), name="post_detail"),
    path('posts/new/', PostCreate.as_view(), name="post_create"),
    path('accounts/profile/update/', UpdateProfile.as_view(), name="update_profile"), 
    path('cities/<int:pk>/', CitiesView.as_view(), name="cities_view"),
    

]