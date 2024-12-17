from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewItemForm, ProductImagesForm
from django.contrib import messages
from core.models import Category, Product, ProductImages, Follow, Stream, Notification # Assuming ProductImage is your image model
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import JsonResponse
from userauths.models import Profile
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def Productitem(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        image_form = ProductImagesForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            try:
                with transaction.atomic():
                    product = form.save(commit=False)  # Create product instance but don't save yet
                    product.user = request.user
                    product.save()  # Save the product to the database
                    form.save_m2m()  # Save the ManyToMany fields like tags

                    # Handle the images
                    images = request.FILES.getlist('images')
                    for image in images:
                        ProductImages.objects.create(product=product, images=image)

                    # Create notifications for followers
                    followers = Follow.objects.filter(following=request.user)
                    for follower in followers:
                        Notification.objects.create(
                            user=follower.follower,
                            title="New Product Added",
                            message=f"{request.user.username} added a new product: {product.title}",
                        )

                messages.success(request, "Product and images added successfully")
                return redirect('core:index')

            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:  
            messages.error(request, "Please correct the errors below.")
            print("Form Errors: ", form.errors)
            print("Image Form Errors: ", image_form.errors)

    else:
        form = NewItemForm()
        image_form = ProductImagesForm()

    context = {
        'form': form,
        'image_form': image_form,
        'categories': categories,
    }

    return render(request, "items/sell.html", context)

def follow_unfollow(request, user_id):
    user_to_follow_unfollow = get_object_or_404(User, id=user_id)
    follow_obj = Follow.objects.filter(follower=request.user, following=user_to_follow_unfollow)

    if follow_obj.exists():
        # Unfollow logic
        follow_obj.delete()
        # Delete the stream entry for the unfollow action
        Stream.objects.filter(user=request.user, following=user_to_follow_unfollow).delete()
        message = f'You have unfollowed {user_to_follow_unfollow.username}.'
    else:
        products = Product.objects.filter(user=user_to_follow_unfollow)[:10]

        # Follow logic
        Follow.objects.create(follower=request.user, following=user_to_follow_unfollow)
        # Create a stream entry for the follow action
        with transaction.atomic():
            for product in products:
             Stream.objects.create(prod=product, user=request.user, following=user_to_follow_unfollow, date=timezone.now())
             
             # Create a notification for the user being followed
            Notification.objects.create(
                user=user_to_follow_unfollow,  # The person receiving the notification (fred)
                 title="New Follower", 
                message=f'{request.user.username} followed you.'  # Notification message: "john followed you."
            )
        message = f'You have followed {user_to_follow_unfollow.username}.'
    
    # Get the 'next' parameter from the URL, or use the referrer
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)



def save_product(request, pid):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=pid)
        profile = Profile.objects.get(user=request.user)

        if product in profile.saved_products.all():
            profile.saved_products.remove(product)
            saved = False
            message = "Product removed from saved items."
        else:
            profile.saved_products.add(product)
            saved = True
            message = "Product added to saved items."

        return JsonResponse({'saved': saved, 'message': message})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required
def EditProduct(request, pid):
    product = get_object_or_404(Product, pid=pid, user=request.user)
    existing_images = product.p_image.all()  # Access the images using the related name

    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES, instance=product)
        image_form = ProductImagesForm(request.POST, request.FILES)  

        # Handle deletion of selected images
        if 'delete_images' in request.POST:
            delete_images = request.POST.getlist('delete_images')  # List of image IDs to delete
            for image_id in delete_images:
                try:
                    image = ProductImages.objects.get(id=image_id)
                    image.delete()  # Delete the image from the database
                except ProductImages.DoesNotExist:
                    messages.error(request, "Image does not exist.")

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            
            # Save new images
            images = request.FILES.getlist('images')  # Get the uploaded images
            if images:
                for image in images:
                    ProductImages.objects.create(product=product, images=image)
            
            messages.success(request, "Product updated successfully")
            return redirect('core:dashboard')
        
    else:
        form = NewItemForm(instance=product)
        image_form = ProductImagesForm()

    context = {
        "form": form,
        "image_form": image_form,
        "product": product,
        "existing_images": existing_images,
    }
    return render(request, 'items/edit-sell.html', context)
