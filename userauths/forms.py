from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Your Fullname',
            'class': 'form-control'
        }))
    email = forms.EmailField( widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email Address',
            'class': 'form-control'
        }))
    password1 = forms.CharField( widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Your Password',
            'class': 'form-control'
        }))
    password2 = forms.CharField( widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Your Password',
            'class': 'form-control'
        }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']
        
class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))
    location = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your location"}))
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"id": "input-file", "accept": "image/jpeg, image/png, image/jpg", 'style': 'display:none;'})
    )
    
    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone', 'location']
