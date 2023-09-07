from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),

    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
     path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('my_order/', views.my_order, name='my_order'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders_detail/<int:order_id>/', views.orders_detail, name='orders_detail'),
    path('return_detail/<int:id>/', views.return_detail, name='return_detail'),
    path('cancel_order_request/<int:id>/', views.cancel_order_request, name='cancel_order_request'),
    path('customer_care/', views.customer_care, name='customer_care'),
    path('order_tract_detail/<int:id>/', views.order_tract_detail, name='order_tract_detail'),
    path('order_return/<int:id>/', views.order_return, name='order_return'),
    path('add_account/<int:id>/', views.add_account, name='add_account'),
    path('return_complete/<int:id>/', views.return_complete, name='return_complete'),


    





]