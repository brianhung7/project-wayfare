from django.urls import path
from . import views
from .views import Home, Signup, Profile


urlpatterns = [
	path('', Home.as_view(), name="home"),
    path('accounts/signup/', Signup.as_view(), name="signup"),
    path('accounts/profile/', Profile.as_view(), name="profile"),

]