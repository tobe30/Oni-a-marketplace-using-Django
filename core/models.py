from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import shortuuid
from taggit.managers import TaggableManager


STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

CONDITION = (
    ("new", "new"),
    ("used", "used"),
    ("old", "old"),
    ("refurbished", "refurbished"),
    ("renovated", "renovated"),

)

TRANSACTION_STATUS = (
    ("failed", "failed"),
    ("completed", "completed"),
    ("pending", "pending"),

)

# Create your models here.
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="ct12")
    title = models.CharField(max_length=100, default="Electronics")

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.title

####brand####
class Brand(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural ='Brand'

    def __str__(self):
        return self.name
    
class Product(models.Model):

    pid = ShortUUIDField(unique=True, length=10, max_length=20,  alphabet="pid123")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=user_directory_path, default="default.jpg")
    youtube_url = models.URLField(null=True, blank=True)  # Optional YouTube link
    views = models.IntegerField(default=0)


    # General Optional Fields
    brand = models.ForeignKey(Brand, related_name='brand', on_delete=models.CASCADE)
    model = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    condition = models.CharField(max_length=50, choices=CONDITION, default="none")  # New, Used, Refurbished
    size = models.CharField(max_length=50, null=True, blank=True)  # For clothes, furniture, etc.
    color = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)  # For real estate, houses, etc.
    warranty = models.CharField(max_length=100, null=True, blank=True)  # For gadgets, appliances, etc.
    features = models.TextField(null=True, blank=True)  # For specific features like 'Bluetooth, GPS'
    
    # Vehicle-Specific Fields (Cars, Motorbikes, etc.)
    mileage = models.IntegerField(null=True, blank=True)
    transmission = models.CharField(max_length=50, null=True, blank=True)  # Automatic, Manual
    fuel_type = models.CharField(max_length=50, null=True, blank=True)  # Petrol, Diesel, Electric
    engine_size = models.CharField(max_length=50, null=True, blank=True)
    number_of_doors = models.IntegerField(null=True, blank=True)
    number_of_seats = models.IntegerField(null=True, blank=True)
    
    # Real Estate-Specific Fields (Houses, Apartments, Land)
    property_type = models.CharField(max_length=100, null=True, blank=True)  # Apartment, Villa, Land
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    square_feet = models.IntegerField(null=True, blank=True)
    lot_size = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    
    # Electronics-Specific Fields (Phones, Laptops, Gadgets)
    screen_size = models.CharField(max_length=50, null=True, blank=True)
    battery_life = models.CharField(max_length=50, null=True, blank=True)
    storage_capacity = models.CharField(max_length=50, null=True, blank=True)
    ram = models.CharField(max_length=50, null=True, blank=True)
    processor = models.CharField(max_length=50, null=True, blank=True)
    camera_quality = models.CharField(max_length=50, null=True, blank=True)
    
    # Furniture-Specific Fields (Beds, Sofas, Tables, etc.)
    material = models.CharField(max_length=100, null=True, blank=True)  # Wood, Metal, Plastic
    dimensions = models.CharField(max_length=100, null=True, blank=True)
    weight = models.CharField(max_length=50, null=True, blank=True)
    
    # Clothes-Specific Fields
    clothing_size = models.CharField(max_length=50, null=True, blank=True)  # Small, Medium, Large
    fabric_type = models.CharField(max_length=100, null=True, blank=True)  # Cotton, Wool, Synthetic
    
    # Toy-Specific Fields
    age_group = models.CharField(max_length=50, null=True, blank=True)  # 3-5 years, 6-8 years, etc.
    safety_standards = models.CharField(max_length=100, null=True, blank=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)
    
    # General Metadata
    tags = TaggableManager(blank=True)  # For search optimization

    def __str__(self):
        return self.title
    
    def product_Image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, related_name="p_image", on_delete=models.SET_NULL, null=True)
    date  =  models.DateTimeField(auto_now_add=True)


    class meta:
        verbose_name_plural = "Product Images"
        
        
################## folling and followers ###############

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stream_user")
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()
    
    def __str__(self):
        prod_title = self.prod.title if self.prod else "No Product"
        return f"{self.user.username} sees {prod_title} from {self.following.username}"
    
    
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="producr_likes")
    
    def __str__(self):
        return f"{self.user.username} likes {self.prod.title}"
    
    
############## Comments ####################

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Comments"
        
################# wallet #############

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_id = ShortUUIDField(unique=True, length=7, max_length=25, prefix="ONI", alphabet="1234567890")  # Shorter Wallet ID
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.user}"
    
class WalletTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reciever')  # Optional recipient for transfers
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sender')     
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=TRANSACTION_STATUS, max_length=100, default="pending")
    transaction_type = models.CharField(max_length=10, choices=(('credit', 'Credit'), ('debit', 'Debit'), ('deposited', 'Deposited'), ('purchased', 'purchased'), ('bought', 'bought')))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
def create_account(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

# SIGNAL: Create stream entry when a new product is posted
@receiver(post_save, sender=Product)
def create_stream_on_new_product(sender, instance, created, **kwargs):
    if created:
        # Get followers of the product owner
        followers = Follow.objects.filter(following=instance.user)
        
        # Create a stream entry for each follower
        for follow in followers:
            Stream.objects.create(
                following=instance.user,
                user=follow.follower,
                prod=instance,
                date=timezone.now()
            )
post_save.connect(create_account, sender=User)
