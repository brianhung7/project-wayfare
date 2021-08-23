from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import View
from django.views.generic import DetailView
from .models import Post, City, Profile
from django.db import models
from django.contrib.auth.models import User


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileCreateForm
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
        signup_form = UserCreationForm()
        profile_form = ProfileUpdateForm()
        context = {"signup_form": signup_form, "profile_form":profile_form}
        return render(request, "registration/signup.html", context)


    def post(self,request):
        signup_form = UserCreationForm(request.POST)
        profile_form = ProfileCreateForm(request.POST)
        if signup_form.is_valid():
            # create our user in the database
            user = signup_form.save()
            #user.refresh_from_db()  # load the profile instance created by the signal

            #print(user)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            #print(profile)
            user.save()
            login(request, user)
            return redirect("profile_view")
        else:
            context = {"signup_form": signup_form, "profile_form": profile_form}
            return render(request, "registration/signup.html", context)


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user=self.request.user)
        context['cities'] = City.objects.all

        return context


@method_decorator(login_required, name='dispatch')
class UpdateProfile(UpdateView):
    #get route -> Handles displaying of user and profile update forms
    def get(self, request):
        #request.user -> The current logged in user
        #request.user.email -> The current users email
        # form_one = UserUpdateForm()
        # form_two = ProfileUpdateForm()
        context = {
            "user": request.user,
            'cities': City.objects.all
        }
        return render(request, "update/updateUser.html", context)

    #post route -> saves form information and retuns to the user profile page
    def post(self, request):
        Profile.objects.filter(user = request.user).update(current_city = request.POST["current_city"])
        if str(request.user)==request.POST["username"] or not User.objects.filter(username=request.POST["username"]):
            User.objects.filter(username = request.user).update(username = request.POST["username"])
            return redirect('profile_view')
        else:
            context = {"error": "Username already taken", 'cities':City.objects.all}
            return render(request,"update/updateUser.html", context)

        
        return redirect('profile_view')


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["city_list"] = City.objects.all()
        post_key = self.kwargs['pk']
        post_creator = Post.objects.get(id=post_key).user.username
        context["post_creator"] = post_creator
        return context

class MainUserCity(View):

    def get(self, request):
        # current_user = Profile.objects.filter(user = request.user)[0] #.get('current_city_id')
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print(current_user)
        return redirect('/cities/1/')

@method_decorator(login_required, name='dispatch')
class CitiesView(DetailView):
    model = City
    template_name = "cities_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_key = self.kwargs['pk']
        #print(self.request.GET.get('pk'))
        context['city_list'] = City.objects.all()
        context['city_posts'] = Post.objects.filter(city=pk_key)
        
        return context

@method_decorator(login_required, name='dispatch')
class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content', 'city']
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        print("SUCCESS URL")
        return reverse("post_detail", kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'city']
    template_name = 'post_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #if the current user != the user who made the post, send back to the PostDetail view
        post_key = self.kwargs['pk']
        post_creator = Post.objects.get(id=post_key).user.username
        context["post_creator"] = post_creator
        return context

    def get_success_url(self):
        return reverse("post_detail", kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class PostDelete(DeleteView):
    model = Post
    template_name = "post_delete_confirmation.html"
    success_url = "/cities/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #if the current user != the user who made the post, send back to the PostDetail view
        post_key = self.kwargs['pk']
        post_creator = Post.objects.get(id=post_key).user.username
        context["post_creator"] = post_creator
        return context


class ProfileViewOther(DetailView):
    model = Profile
    template_name = 'profile_other.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user_id=kwargs['object'].pk)
        context['cities'] = City.objects.all
        if self.request.user.profile.pk == self.kwargs['pk']:
            context['profile_is_user'] = True
        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     pk_key = self.kwargs['pk']
    #     if self.request.user.pk == pk_key:
    #         return redirect("profile_view")
    #     return context
    # def get(self,request,*args,**kwargs):
    #     current_user_pk = self.request.user.pk
    #     user_lookup_pk = kwargs['pk']
    #     if current_user_pk == user_lookup_pk:
    #         return redirect('profile_view')
    #     return print("Hello")


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        signup_form = UserCreationForm()
        profile_form = ProfileUpdateForm()
        context["signup_form"] = signup_form
        context["profile_form"] = profile_form
        return context