from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views import View
from django.views.generic import DetailView
from .models import Post, City, Profile
from django.db import models
from django.contrib.auth.models import User


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileCreateForm
# Create your views here.
class Home(TemplateView):
    template_name= 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        signup_form = UserCreationForm()
        profile_form = ProfileUpdateForm()
        context["signup_form"] = signup_form
        context["profile_form"] = profile_form
        return context

class Signup(View):

    def get(self,request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)


    def post(self,request):
        form = UserCreationForm(request.POST)
        profile_form = ProfileCreateForm(request.POST)
        if form.is_valid():
            # create our user in the database
            user = form.save()
            #user.refresh_from_db()  # load the profile instance created by the signal

            print(user)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            print(profile)
            user.save()
            login(request, user)
            return redirect("home")
        else:
            context = {"form": form, "profile_form": profile_form}
            return render(request, "registration/signup.html", context)


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user=self.request.user)

        return context


class UpdateProfile(UpdateView):
    #get route -> Handles displaying of user and profile update forms
    def get(self, request):
        #request.user -> The current logged in user
        #request.user.email -> The current users email
        # form_one = UserUpdateForm()
        # form_two = ProfileUpdateForm()
        context = {
            "user": request.user
        }
        return render(request, "update/updateUser.html", context)

    #post route -> saves form information and retuns to the user profile page
    def post(self, request):
        
        Profile.objects.filter(user = request.user).update(current_city = request.POST["current_city"])
        User.objects.filter(username = request.user).update(username = request.POST["username"])
        
        return redirect('profile_view')


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post"] = Post.objects.get()
    #     return context