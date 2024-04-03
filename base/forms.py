from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class UserRegistrationForm(UserCreationForm): 
    
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'profile_photo', 'bio']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser 
        fields= ['username','profile_photo','bio']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body',)
        widgets = {
            'comment_body': forms.TextInput(attrs={'class': 'form-control'}),
        }
