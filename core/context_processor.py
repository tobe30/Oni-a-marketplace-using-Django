from core.models import Category, Product, Notification
from django.db.models import Min, Max

def default(request):
    # Get all categories
    category = Category.objects.all()
    
    # Get the minimum and maximum price from the Product model
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    
    # Check if the user is authenticated before querying for notifications
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-date')
    else:
        notifications = []  # Empty list if the user is not authenticated
    
    return {
        "category": category,
        "min_max_price": min_max_price,
        "notifications": notifications,
    }
