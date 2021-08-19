from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views import View
from django.views.generic import DetailView
from .models import Post, City, Profile


from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, ProfileUpdateForm
# Create your views here.
class Home(TemplateView):
    template_name= 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        signup_form = UserCreationForm()
        context["signup_form"] = signup_form
        return context

class Signup(View):

    def get(self,request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)


    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # create our user in the database
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            #user.profile = Profile(user, 'current_city_id' = 1,)
            # user.profile.current_city = 1
            # user.profile.avatar = 'https://i.imgur.com/QMxdIUh.jpeg' 
            user.save()
            login(request, user)
            return redirect("home")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)


class Profile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user=self.request.user)

        return context


class UpdateProfile(View):
    #get route -> Handles displaying of user and profile update forms
    def get(self, request):
        form_one = UserUpdateForm()
        form_two = ProfileUpdateForm()
        context = {
            "form_one": form_one,
            "form_two": form_two
        }
        return render(request, "update/updateUser.html", context)

    #post route -> saves form information and retuns to the user profile page
    def post(self, request):
        form_one = UserUpdateForm(request.POST)
        form_two = ProfileUpdateForm(request.POST)
        print(request.POST)
        if form_one.is_valid() and form_two.is_valid():
            form_one.save()
            form_two.save()
            return redirect("profile")

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post"] = Post.objects.get()
    #     return context