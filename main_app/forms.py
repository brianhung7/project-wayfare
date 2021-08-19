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
        fields = ['current_city', 'avatar']

    #Saving issue in form_two.save(), overwriting to supply correct info
    def save(self, user=None):
        user_profile = super(ProfileUpdateForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile