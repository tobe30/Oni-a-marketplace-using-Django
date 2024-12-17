from django.urls import path
from . import views

app_name = 'core'

urlpatterns =[
    path('', views.index, name='index'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('seller/<str:username>', views.SellerProfile, name='seller_profile'),
    path('sellers/', views.Seller, name='sellers'),
    path('like/<int:pid>/', views.like_product, name='like_product'),
    path('products/<pid>', views.prod_details, name='product-details'),
    path('products', views.Shops, name='products'),
    path('following', views.following, name='following'),
    path('category-shops/<cid>/', views.category_shop, name='cat-shop'),
    path('dashboard/wallet', views.Wallets, name='wallet'),
    path('deposit/', views.process_payment, name='deposit_funds'),
    path('deposit/', views.process_payment, name='deposit_funds'),
    path('wallet/send/', views.process_send_funds, name='process_send_funds'),
    path('purchase/<pid>', views.Purchase, name='purchase'),
    path('process_purchase/<str:pid>/', views.process_purchase, name='process_purchase'),
    path('notifications/', views.notifications_view, name='notifications'),
    
    #tags
    path("products/tag/<slug:tag_slug>/", views.tag_list, name="tags"),
    
    
    #search
    path("search/", views.search_view, name="search"),
    
    #settings
    path("settings/", views.settings_view, name="settings"),

    
    

    
    

    
    
    
    
    
    
    
    

]