from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns =[
    path("message/<int:pid>/", views.Chat_view, name="chat_view"),
    path("message/", views.new_message, name="new")
]