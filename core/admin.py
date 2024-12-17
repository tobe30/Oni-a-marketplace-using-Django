from django.contrib import admin
from core.models import ProductImages, Product, Category, Brand, Follow, Stream, Likes, Comments, Wallet, WalletTransaction, Notification


# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_Image', 'price', 'category', 'features', 'product_status', 'pid']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'prod', 'review']
    
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'wallet_id', 'balance']
    
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'sender', 'receiver', 'status', 'amount', 'transaction_type']
    
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message','date', 'title']
    


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(Likes)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
admin.site.register(Notification, NotificationAdmin)




