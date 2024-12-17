from django.shortcuts import render, get_object_or_404, redirect
from core.models import Product
from chat.models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Chat, Message, Product

@login_required
def Chat_view(request, pid):
    # Retrieve the product or raise a 404 error if not found
    product = get_object_or_404(Product, id=pid)

    # Get or create a chat instance for the product
    chat, created = Chat.objects.get_or_create(product=product)

    # Ensure the participants are added to the chat
    # Add the product owner and the current user (buyer) as participants
    product_owner = product.user  # Assuming 'user' is the foreign key to the seller in Product
    if request.user not in chat.participants.all():
        chat.participants.add(request.user)
    if product_owner not in chat.participants.all():
        chat.participants.add(product_owner)

    buyer = chat.participants.exclude(id=product_owner.id).first()
    
    chats = Chat.objects.filter(participants=request.user)
    chat_participants = []
    for chat_item in chats:
        other_participant = chat_item.participants.exclude(id=request.user.id).first()
        if other_participant:
            chat_participants.append({
                'participant': other_participant,
                'last_message': chat_item.messages.last(),
                'chat': chat_item
            })
    
    # Handle message submission
    if request.method == 'POST':
        content = request.POST.get('content')  # Text message
        image = request.FILES.get('image')  # Image upload

        # Check if a text message was submitted
        if content:
            Message.objects.create(chat=chat, sender=request.user, content=content)

        # Check if an image was uploaded
        elif image:
            Message.objects.create(chat=chat, sender=request.user, image=image)

        # Redirect to the chat view to display the new message
        return redirect('chat:chat_view', pid=product.id)

    # Automatically send a default message if a new chat was created
    if created:
        default_message = "Is this available?"
        Message.objects.create(chat=chat, sender=request.user, content=default_message)

    # Retrieve all messages associated with the chat, ordered by timestamp
    messages = chat.messages.all().order_by('timestamp')

    # Pass context variables to the template
    context = {
        "product": product,
        "messages": messages,
        'user_profile': request.user.profile,
        'product_owner': product_owner,
        'buyer': buyer,
        'chat_participants': chat_participants,
    }

    return render(request, 'chat/message.html', context)

@login_required
def new_message(request):
    
    chats = Chat.objects.filter(participants=request.user)
    chat_participants = []
    for chat_item in chats:
        other_participant = chat_item.participants.exclude(id=request.user.id).first()
        if other_participant:
            chat_participants.append({
                'participant': other_participant,
                'last_message': chat_item.messages.last(),
                'chat': chat_item
            })
    context = {
        'chat_participants': chat_participants,
        
    }
    return render(request, 'chat/new-message.html', context)