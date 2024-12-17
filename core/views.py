from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from userauths.models import Profile
from django.template.loader import render_to_string
from core.models import Product, Follow, Likes, Comments, Category, Stream, Wallet, WalletTransaction, Notification
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
from core.forms import CommentForm, PasswordChangeForm, DeactivateAccountForm
from django.db.models import Q
from django.db.models import Min, Max
from django.db.models import Count, Sum, F, Q
from django.db.models import ExpressionWrapper, IntegerField
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.contrib.auth import update_session_auth_hash



# Create your views here.

def index(request):
    user = request.user
    
    # Get all published products, ordered by id
    product = Product.objects.filter(product_status="published").order_by("-id")
    
    # Get liked products if user is authenticated
    liked_products = Likes.objects.filter(user=user).values_list('prod_id', flat=True) if user.is_authenticated else []
    
    # Exclude the logged-in user from the profiles, if authenticated
    profiles = Profile.objects.all()
    if user.is_authenticated:
        profiles = profiles.exclude(user=user)
        # Get list of users the current user is following
        user_following = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
    else:
        user_following = []

    # Add follow status to each profile
    for profile in profiles:
        profile.is_following = profile.user.id in user_following

    # Trending products based on a combination of likes and views
    trending_products = Product.objects.filter(product_status="published").annotate(
        trending_score=F('likes') + F('views')  # Combine likes and views for trending score
    ).order_by('-trending_score')[:5]  # Get top 5 trending products

    # Top sellers based on total product views
    top_sellers = Profile.objects.annotate(
    total_views=Sum('user__product__views'),
    total_likes=Count('user__product__likes'),
    total_comments=Count('user__comments')
    ).annotate(
    combined_score=F('total_views') + F('total_likes') + F('total_comments')
    ).filter(
    Q(total_views__gt=0) | Q(total_likes__gt=0) | Q(total_comments__gt=0)  # Exclude users with no activity
    ).order_by('-combined_score')[:6]

    context = {
        "product": product,
        "profiles": profiles,
        'liked_products': liked_products,
        "trending_products": trending_products,
        "top_sellers": top_sellers
    }

    return render(request, "core/index.html", context)


#Dashboard for the user

@login_required
def Dashboard(request):
    
    user_profile = Profile.objects.get(user=request.user)
    
     # Get current month and year
    now = timezone.now()
    current_month = now.month
    current_year = now.year
    
    products = Product.objects.filter(user=request.user, updated_at__month=current_month, updated_at__year=current_year)
    saved =user_profile.saved_products.all()
    
    total_views = products.aggregate(Sum('views'))['views__sum'] or 0
    liked_products = Likes.objects.filter(user=request.user).values_list('prod_id', flat=True)
    
    # Get current month and year
    now = timezone.now()
    current_month = now.month
    current_year = now.year
    
    followers_count = Follow.objects.filter(following=user_profile.user).count()
    following_count = Follow.objects.filter(follower=user_profile.user).count()
    followers = Follow.objects.filter(following=user_profile.user)
    
    context = {
        "user_profile":user_profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'followers':followers,
        'products':products,
        'total_views':total_views,
        'liked_products':liked_products,
        'saved':saved
    }
    
    
    return render(request, "core/dashboard.html", context)


#seller profile
def SellerProfile(request, username):
    
    user = request.user
    try:
        seller = User.objects.get(username=username)
    except User.DoesNotExist:
        
        messages.warning(request, "User does not exist")
        return redirect('core:seller_profile', username=request.user.username) 
    
    profile = get_object_or_404(Profile, user=seller)
    
    products = Product.objects.filter(user=seller)
    
    followers_count = Follow.objects.filter(following=seller).count()
    following_count = Follow.objects.filter(follower=seller).count()
    followers = Follow.objects.filter(following=seller)
    
    
    # Check follow status
    user_following = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True) if request.user.is_authenticated else []
    
    # Set follow status for the seller's profile
    profile.is_following = profile.user.id in user_following
    
    context = {
        'profile': profile,
        'products': products,
        'followers_count': followers_count,
        'following_count': following_count,
        'followers':followers
    }
    
    return render(request, "core/seller-profile.html", context)

#seller
def Seller(request):
    user = request.user
    
    profiles = Profile.objects.all()  # Exclude the logged-in user

    user_following = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True) if request.user.is_authenticated else []

    # Add follow status to each profile
    for profile in profiles:
        profile.is_following = profile.user.id in user_following
    
    context= {
        "profiles":profiles
    }

    return render(request, "core/sellers.html", context)

#liked product
def like_product(request, pid):
    product = get_object_or_404(Product, id=pid)
    user = request.user

    # Check if the user already liked the product
    existing_like = Likes.objects.filter(user=user, prod=product).first()
    
    if existing_like:
        # If the user has already liked the product, remove the like
        existing_like.delete()
        liked = False
    else:
        # Otherwise, add a new like
        Likes.objects.create(user=user, prod=product)
        liked = True
        
        # Update like count for the product
    like_count = Likes.objects.filter(prod=product).count()
    product.likes = like_count
    product.save()
    
    if liked:
        Notification.objects.create(
            user=product.user,  # The owner of the product
            title="Product Liked",  # Notification title
            message=f'{request.user.username} liked your product "{product.title}".'  # Notification message
        )

    return JsonResponse({'liked': liked, 'like_count': like_count})


def prod_details(request, pid):
    product = get_object_or_404(Product, pid=pid)
    profile = Profile.objects.filter(user=product.user).first()

    # Handle likes for authenticated users
    liked_products = []
    liked = False

    if request.user.is_authenticated:
        liked_products = Likes.objects.filter(user=request.user).values_list('prod_id', flat=True)
        liked = Likes.objects.filter(user=request.user, prod=product).exists()
    
    comments = Comments.objects.filter(prod=product).order_by("-date")
    
    # Track if the product has been viewed by the user using session
    viewed_products = request.session.get('viewed_products', [])
    
    if pid not in viewed_products:
        product.views += 1  # Increment the view count
        product.save()  # Save the updated view count
        viewed_products.append(pid)  # Add product ID to the session
        request.session['viewed_products'] = viewed_products
    
    # Handle comments
    comments_form = CommentForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comments_form = CommentForm(request.POST)
        if comments_form.is_valid():
            # Save the comment to the database
            comment = comments_form.save(commit=False)
            comment.prod = product
            comment.user = request.user
            comment.save()
            return redirect('core:product-details', pid=product.pid)
    
    # Check if the user is allowed to make a review (only one review per product)
    make_review = True
    if request.user.is_authenticated:
        user_review_count = Comments.objects.filter(user=request.user, prod=product).count()
        if user_review_count > 0:
            make_review = False
    
    p_image = product.p_image.all()

    context = {
        "p": product,
        "profile": profile,
        "p_image": p_image,
        "liked": liked,  # Pass the liked status to the template
        "liked_products": liked_products,
        "comments_form": comments_form,
        "make_review": make_review,
        "comments": comments
    }

    return render(request, 'core/details.html', context)




@login_required
def Shops(request):
    query = request.GET.get('query', '')
    categories = request.GET.getlist('categories')
    max_price = request.GET.get('max_price', None)
    sort_by = request.GET.get('sort', '')

    products = Product.objects.filter(product_status="published")
    profile = Profile.objects.get(user=request.user)
    liked_products = Likes.objects.filter(user=request.user).values_list('prod_id', flat=True)

    # Apply search filter
    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if categories:
        products = products.filter(category__id__in=categories).distinct()

    # Handle max_price: convert it to a number and ensure correct filtering
    try:
        if max_price is not None and max_price.isdigit():
            max_price = float(max_price)  # Convert to float for comparison
            products = products.filter(price__lte=max_price)
    except ValueError:
        pass  # Invalid input in price filter

    # Sorting options based on the likes field
    if sort_by == 'top_liked':
        products = products.order_by('-likes')  # Most liked products first
    elif sort_by == 'low_liked':
        products = products.order_by('likes')  # Least liked products first

    # Get min and max prices for the slider
    min_max_price = {
        'price__min': products.aggregate(Min('price'))['price__min'] or 0,
        'price__max': products.aggregate(Max('price'))['price__max'] or 0,
    }

    categories = Category.objects.all()

    context = {
        'product': products,
        'min_max_price': min_max_price,
        'category': categories,
        'query': query,
        'profile': profile,
        'liked_products': liked_products,
    }
    return render(request, 'core/shops.html', context)

def search_view(request):
    query = request.GET.get("q")
    categories = request.GET.getlist('categories')
    max_price = request.GET.get('max_price', None)
    sort_by = request.GET.get('sort', '')
    
    profile = None
    liked_products = []

    # Check if the user is authenticated
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        liked_products = Likes.objects.filter(user=request.user).values_list('prod_id', flat=True)
    
    if categories:
        products = products.filter(category__id__in=categories).distinct()
        
    if query:
        # Perform the search only if there is a query
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        # If there's no query, you can return all products or an empty queryset
        products = Product.objects.none()
        
    # Handle max_price: convert it to a number and ensure correct filtering
    try:
        if max_price is not None and max_price.isdigit():
            max_price = float(max_price)  # Convert to float for comparison
            products = products.filter(price__lte=max_price)
    except ValueError:
        pass  # Invalid input in price filter

    # Sorting options based on the likes field
    if sort_by == 'top_liked':
        products = products.order_by('-likes')  # Most liked products first
    elif sort_by == 'low_liked':
        products = products.order_by('likes')  # Least liked products first

    # Get min and max prices for the slider
    min_max_price = {
        'price__min': products.aggregate(Min('price'))['price__min'] or 0,
        'price__max': products.aggregate(Max('price'))['price__max'] or 0,
    }

    categories = Category.objects.all()

    context = {
        'query': query,  # Pass the query correctly to the template
        'products': products,  # Correctly pass the products queryset
        'min_max_price': min_max_price,
        'category': categories,
        'query': query,
        'profile': profile,
        'liked_products': liked_products,
    }

    return render(request, 'core/search.html', context)


def following(request):
    user = request.user

    # Get the product IDs of users you are following
    following_products = Stream.objects.filter(user=user).values_list('prod_id', flat=True)
    liked_products = Likes.objects.filter(user=user).values_list('prod_id', flat=True)

    # Get products from the followed users
    prod_items = Product.objects.filter(id__in=following_products, product_status="published")

    # Get query parameters for sorting and filtering
    query = request.GET.get('query', '')
    sort_by = request.GET.get('sort', '')
    max_price = request.GET.get('max_price', None)
    categories = request.GET.get('categories')
    
    #search query
    if query:
        prod_items = prod_items.filter(title__icontains=query)
        
    if categories:
        prod_items = prod_items.filter(category__id__in=categories).distinct()

    # Sort products
    if sort_by == 'top_liked':
        prod_items = prod_items.annotate(like_count=Count('likes')).order_by('-like_count')
    elif sort_by == 'low_liked':
        prod_items = prod_items.annotate(like_count=Count('likes')).order_by('like_count')

    # Filter by max price
    if max_price is not None and max_price.isdigit():
        max_price = float(max_price)
        prod_items = prod_items.filter(price__lte=max_price)

    # Get min and max prices for the slider
    min_max_price = prod_items.aggregate(price__min=Min('price'), price__max=Max('price'))

    print("Following product IDs:", following_products)
    print("Filtered product IDs:", prod_items.values_list('id', flat=True))

    # Retrieve all categories for filtering (if needed)
    categories = Category.objects.all()

    context = {
        'product': prod_items,
        'liked_products': liked_products,
        'profile': Profile.objects.get(user=request.user),
        'min_max_price': min_max_price,
        'category': categories,
    }
    return render(request, 'core/following.html', context)


def category_shop(request, cid):
    query = request.GET.get('query', '')
    selected_categories = request.GET.getlist('categories')
    max_price = request.GET.get('max_price', None)
    sort_by = request.GET.get('sort', '')

    # Fetching the category based on cid
    categories = get_object_or_404(Category, cid=cid)
    
    # Filter products for the selected category and published products
    product = Product.objects.filter(category=categories, product_status="published")
    
    # Get the profile and liked products for the logged-in user
    profile = None
    liked_products = []

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        liked_products = Likes.objects.filter(user=request.user).values_list('prod_id', flat=True)

    # Apply search filter
    if query:
        product = product.filter(title__icontains=query)

    # Filter products based on selected categories (if any)
    if selected_categories:
        product = product.filter(category__id__in=selected_categories).distinct()

    # Filter by maximum price
    try:
        if max_price is not None and max_price.isdigit():
            max_price = float(max_price)
            product = product.filter(price__lte=max_price)
    except ValueError:
        pass  # Handle invalid max_price input gracefully

    # Apply sorting based on likes
    if sort_by == 'top_liked':
        product = product.order_by('-likes')
    elif sort_by == 'low_liked':
        product = product.order_by('likes')

    # Get minimum and maximum prices for the price slider
    min_max_price = {
        'price__min': product.aggregate(Min('price'))['price__min'] or 0,
        'price__max': product.aggregate(Max('price'))['price__max'] or 0,
    }

    # Fetch all categories to display as filter options
    all_categories = Category.objects.filter(cid=categories)

    context = {
        'product': product,
        'min_max_price': min_max_price,
        'categories': categories,
        'all_categories': all_categories,
        'query': query,
        'profile': profile,
        'liked_products': liked_products,
    }
    
    return render(request, "core/category-shop.html", context)

@login_required
def Wallets(request):
    
    wallet = Wallet.objects.get(user=request.user)
    transactions = WalletTransaction.objects.filter(user=request.user)
    
    context ={
        'wallet':wallet,
        'transactions':transactions
    }
    return render(request, "core/wallet.html", context)

@login_required
def process_payment(request):
    if request.method =='POST':
        amount = request.POST.get('amount')
        
        if amount:
            try:
                amount = Decimal(amount)
                if amount > 0:
                    wallet = Wallet.objects.get(user=request.user)
                    
                    #add money
                    wallet.balance += Decimal(amount)
                    wallet.save()
                    
                    
                    sender = request.user
                    receiver = request.user
                    
                    WalletTransaction.objects.create(
                        user=request.user,
                        sender=sender,
                        receiver=receiver,
                        amount=amount,
                        transaction_type='deposited',  # Since it's a deposit, it's a credit
                        status='completed'  # Assuming the transaction is completed immediately
                    )
                    
                    Notification.objects.create(
                        user=request.user,
                        title="Deposit Successful",  # Notification title
                        message=f'₦{amount} has been successfully deposited to your wallet.'  # Message to notify the user
                    )
                    
                    messages.success(request, f'₦{amount} has been deposited to your wallet.')
                    return redirect('core:wallet')
                else:
                    messages.error(request, 'Amount must be greater than zero')
                    return redirect('core:wallet')
            except ValueError:
                messages.error(request, 'Invalid amount.')
                return redirect('core:wallet')
        else:
            messages.error(request, 'Please enter a Valid amount')
            return redirect('core:wallet')
    return render(request, 'core/wallet.html')
    

@login_required
def process_send_funds(request):
    if request.method =='POST':
        reciever_wallet_id = request.POST.get('receiver_wallet_id')
        amount = request.POST.get('amount')
        
        if reciever_wallet_id and amount:
            try:
                amount = Decimal(amount)
                if amount > 0:
                    
                    sender_wallet = Wallet.objects.get(user=request.user)
                    
                    if sender_wallet.balance >= amount:
                        try:
                            reciever_wallet = Wallet.objects.get(wallet_id=reciever_wallet_id)
                            
                            
                            sender_wallet.balance -= amount
                            sender_wallet.save()
                            
                            reciever_wallet.balance += amount
                            reciever_wallet.save()
                            
                            sender = request.user
                            receiver = reciever_wallet.user
                            
                            WalletTransaction.objects.create(
                                user=reciever_wallet.user,
                                sender=sender,
                                receiver=receiver,
                                amount=amount,
                                transaction_type='credit',  # Since it's a deposit, it's a credit
                                status='completed'  # Assuming the transaction is completed immediately
                            )
                            
                            WalletTransaction.objects.create(
                                user=request.user,
                                sender=sender,
                                receiver=receiver,
                                amount=amount,
                                transaction_type='debit',  # Since it's a deposit, it's a credit
                                status='completed'  # Assuming the transaction is completed immediately
                            )
                            
                            # Send notification to the sender
                            Notification.objects.create(
                                    user=request.user,
                                    title="Funds Sent",
                                    message=f'₦{amount} has been successfully sent to {receiver.username}.'
                                )
                                
                                # Send notification to the receiver
                            Notification.objects.create(
                                    user=receiver,
                                    title="Funds Received",
                                    message=f'You have received ₦{amount} from {sender.username}.'
                                )
                            
                            
                            messages.success(request,  f'₦{amount} has been sent to {reciever_wallet.user.username}.')
                            return redirect('core:wallet')
                        except Wallet.DoesNotExist:
                            messages.error(request, 'Recipient wallet does not exist.')
                    else:
                        messages.error(request, 'Insufficient balance.')
                else:
                    messages.error(request, 'Amount must be greater than zero.')
            except  Decimal.InvalidOperation:
                 messages.error(request, 'Invalid amount.')
        else:
            messages.error(request, 'Please enter the recipient wallet ID and amount.')
    return redirect('core:wallet')

@login_required
def Purchase(request, pid):
    
    product = get_object_or_404(Product, pid=pid)
    
    wallet = Wallet.objects.get(user=request.user)
    
    context ={
        'product':product,
        'wallet':wallet
    }
    
    
    return render(request, "core/purchase.html", context)

@login_required
def process_purchase(request, pid):
    if request.method == 'POST':
        product = get_object_or_404(Product, pid=pid)
        buyer= request.user
        seller = product.user 
        amount_to_pay = product.price
        
        try:
            buyer_wallet = Wallet.objects.get(user=buyer)
        except Wallet.DoesNotExist:
            messages.error(request, "You don't have a wallet set up.")
            return redirect('purchase', pid=pid)

        # Get the seller's wallet
        try:
            seller_wallet = Wallet.objects.get(user=seller)
        except Wallet.DoesNotExist:
            messages.error(request, "The seller doesn't have a wallet set up.")
            return redirect('purchase', pid=pid)
        
        if buyer_wallet.balance >= amount_to_pay:
            # Deduct the amount from the buyer's wallet
            buyer_wallet.balance -= amount_to_pay
            buyer_wallet.save()

            # Add the amount to the seller's wallet
            seller_wallet.balance += amount_to_pay
            seller_wallet.save()
            
            
            WalletTransaction.objects.create(
                        user=buyer,
                        product=product,
                        amount=amount_to_pay,
                        transaction_type='purchased',  
                        status='completed' 
                    )
            
            WalletTransaction.objects.create(
                        user=seller,
                        receiver = buyer,
                        product=product,
                        amount=amount_to_pay,
                        transaction_type='bought',  
                        status='completed' 
                    )
            Notification.objects.create(
                                    user=buyer,
                                    title="Purchased",
                                    message=f'You Purchased {product.title} for ₦{amount_to_pay}.'
                                )
            
            Notification.objects.create(
                                    user=seller,
                                    title="Bought your product",
                                    message=f'{buyer.username} bought {product.title} for ₦{amount_to_pay}.'
                                )
            
            
            messages.success(request, "Payment successful! You have purchased the product.")
            return redirect('core:wallet')
        else:
            messages.error(request, "Insufficient balance in wallet.")
            return redirect('core:purchase', pid=pid)
    else:
        return redirect('core:purchase', pid=pid)
    

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-date')
    context = {
        'notifications': notifications,
    }
    return render(request, 'core/notification.html', context)

def tag_list(request, tag_slug=None):
    
    products = Product.objects.filter(product_status="published").order_by("-id")  
    
    tags = None
    if tag_slug:
        tags = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tags])

    context = {
        "product": products,
        "tag": tags,

        
    }
    return render(request, "core/tags.html", context)
            
@login_required
def settings_view(request):
    password_form = PasswordChangeForm(user=request.user)  # Use the built-in form
    deactivate_form = DeactivateAccountForm()  # Initialize the deactivate form

    if request.method == 'POST':
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()  # Change the password
                update_session_auth_hash(request, user)  # Important! Keep user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('core:settings')  # Redirect to clear the form
            else:
                # Handle form errors and add them to messages
                for error in password_form.errors.values():
                    messages.error(request, error)
        elif 'deactivate_account' in request.POST:
            deactivate_form = DeactivateAccountForm(request.POST)
            if deactivate_form.is_valid():
                password = deactivate_form.cleaned_data['password']
                if request.user.check_password(password):
                    request.user.delete()
                    messages.success(request, 'Your account has been deactivated.')
                    return redirect('core:index')
                else:
                    messages.error(request, 'Password is incorrect. Please try again.')

    context = {
        'password_form': password_form,
        'deactivate_form': deactivate_form,
    }
    return render(request, 'core/settings.html', context)