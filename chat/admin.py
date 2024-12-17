# admin.py
from django.contrib import admin
from chat.models import Chat, Message




class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender']

admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)

