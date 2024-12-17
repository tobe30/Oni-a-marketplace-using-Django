from django.shortcuts import render, redirect, get_object_or_404
from userauths.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from userauths.models import User, Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

def Registerview(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Access Denied..")
        
        return redirect('')
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your account was created successfully")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("core:index")
    
    else:
        form = UserRegisterForm()
    context ={
        "form":form,
    }
    return render(request, "userauths/sign-up.html", context)

def Loginview(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request,email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in")
                return redirect("core:index")
            else:
                messages.warning(request, "email or password does not exist")
                return redirect("userauths:sign-in")
        except:
            messages.warning(request, f"User with this{email} does not exist")
            
    if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect("core:index")
    return render(request, "userauths/sign-in.html")


def logoutView(request):
      logout(request)
      messages.success(request, "You have been logged out")
      return redirect("userauths:sign-in")
  
@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated successfully")
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)
        
    context = {
        "form":form,
        "profile":profile
    }
    return render(request, "userauths/edit-profile.html", context)
     
@login_required
def profile_view(request, pid):
    profile = get_object_or_404(Profile, id=pid)
    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)
    
    
