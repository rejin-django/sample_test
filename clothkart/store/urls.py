from django.urls import path,include
from . import views


urlpatterns = [
    path('addproduct/',views.addproduct,name='addproduct'),
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_wishlist/<int:product_id>/', views.add_wishlist, name='add_wishlist'),

    
    

]