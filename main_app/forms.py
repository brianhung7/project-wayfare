from django import forms
from django.contrib.auth.models import User
from .models import Profile

# Create forms here
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'current_city', 'avatar']