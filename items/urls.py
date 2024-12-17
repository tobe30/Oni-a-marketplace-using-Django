from django.urls import path
from items import views


app_name = 'items'

urlpatterns = [
   path('', views.Productitem, name='sell'),
   path('follow_unfollow/<int:user_id>/', views.follow_unfollow, name='follow_unfollow'),
   path('saved/<int:pid>/', views.save_product, name='saved'),  # Ensure pid is treated as an integer
   
   #edit product
   path('edit-product/<pid>', views.EditProduct, name='edit_prod'),
   
   
   
]