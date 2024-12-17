from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.Registerview, name="sign-up"),
    path("sign-in/", views.Loginview, name="sign-in"),
    path("sign-out/", views.logoutView, name="sign-out"),
    path("edit-profile/", views.profile_edit, name="edit-profile"),
    path("profile/<int:pid>/", views.profile_view, name="profile"), 
    
    

]