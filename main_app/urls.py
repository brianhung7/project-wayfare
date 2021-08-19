from django.urls import path
from . import views
from .views import Home, Signup, ProfileView, PostDetail, UpdateProfile


urlpatterns = [
	path('', Home.as_view(), name="home"),
    path('accounts/signup/', Signup.as_view(), name="signup"),
    path('accounts/profile/', ProfileView.as_view(), name="profile_view"),
    path('posts/<int:pk>/', PostDetail.as_view(), name="post_detail"),
    path('accounts/profile/update/', UpdateProfile.as_view(), name="update_profile"), 
]