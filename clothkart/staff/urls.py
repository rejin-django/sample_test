from django.urls import path,include
from .import views


urlpatterns=[

    path('',views.staff_home,name='staff_home'),
    path('add_product/',views.add_product,name='add_product'),
    path('add_category/',views.add_category,name='add_category'),
    path('add_product_variation/',views.add_product_variation,name='add_product_variation'),

    path('view_variation/<int:id>/',views.view_variation,name='view_variation'),
    path('variation_delete/<int:id>/',views.variation_delete,name='variation_delete'),
    path('add_product_gallery/',views.add_product_gallery,name='add_product_gallery'),
    path('product_enable/<int:id>/',views.product_enable,name='product_enable'),
    path('product_disable/<int:id>/',views.product_disable,name='product_disable'),
    path('category_delete/<int:id>/',views.category_delete,name='category_delete'),
    path('product/',views.product,name='product'),
     path('product_variation_enable/<int:id>/',views.product_variation_enable,name='product_variation_enable'),
    path('product_variation_disable/<int:id>/',views.product_variation_disable,name='product_variation_disable'),
    path('productgallery_delete/<int:id>/',views.productgallery_delete,name='productgallery_delete'),
    path('add_supplier/',views.add_supplier,name='add_supplier'),
    path('edit_supplier/<int:id>',views.edit_supplier,name='edit_supplier'),
    path('view_supplier/',views.view_supplier,name='view_supplier'),
    path('order_detail_supplier/',views.order_detail_supplier,name='order_detail_supplier'),
    path('order_history_admin/',views.order_history_admin,name='order_history_admin'),
    path('about_product/',views.about_product,name='about_product'),
    path('completed_order/',views.completed_order,name='completed_order'),
    path('confirm_order/',views.confirm_order,name='confirm_order'),
    path('order_history_supplier/',views.order_history_supplier,name='order_history_supplier'),
    path('view_ordered_product/<int:id>/',views.view_ordered_product,name='view_ordered_product'),
    path('view_supplier_order_detail/',views.view_supplier_order_detail,name='view_supplier_order_detail'),
    path('supplier_confirm_order_detail/',views.supplier_confirm_order_detail,name='supplier_confirm_order_detail'),
    path('mainagent_shipment/<int:id>/',views.mainagent_shipment,name='mainagent_shipment'),
    path('admin_verified_orders/', views.admin_verified_orders, name='admin_verified_orders'),
    

    path('confirm_order_supplier/<int:id>/',views.confirm_order_supplier,name='confirm_order_supplier'),
    path('cancel_order_supplier/<int:id>/',views.cancel_order_supplier,name='cancel_order_supplier'),
    path('verify_order/<int:id>/', views.verify_order, name='verify_order'),
    path('verified_orders/', views.verified_orders, name='verified_orders'),
    path('cancel_order/<int:id>/', views.cancel_order, name='cancel_order'),

    path('assigns_to/<int:id>/', views.assigns_to, name='assigns_to'),
    path('add_salesman/', views.add_salesman, name='add_salesman'),
    
    path('edit_assign_to/<int:id>/', views.edit_assign_to, name='edit_assign_to'),
    path('addcorporateagent/', views.addcorporateagent, name='addcorporateagent'),
    path('corporates_shipment/<int:id>/', views.corporates_shipment, name='corporates_shipment'),

  
    path('view_gallery/<int:id>/', views.view_gallery, name='view_gallery'),

   
 

    path('supplier_confirmed_admin_view/', views.supplier_confirmed_admin_view, name='supplier_confirmed_admin_view'),
    path('supplier_cancelled_admin_view/', views.supplier_cancelled_admin_view, name='supplier_cancelled_admin_view'),
    path('shipping_details/<int:id>/', views.shipping_details, name='shipping_details'),
    path('customer_queries_solution/<int:id>/', views.customer_queries_solution, name='customer_queries_solution'),

    path('add_state/', views.add_state, name='add_state'),

    path('add_district/', views.add_district, name='add_district'),
    path('add_mainagent/', views.add_mainagent, name='add_mainagent'),
    path('corporateagent_view/', views.corporateagent_view, name='corporateagent_view'),
    path('customer_queries/', views.customer_queries, name='customer_queries'),
    

     path('mainagent_view/', views.mainagent_view, name='mainagent_view'),
    # path('salesman_view/', views.salesman_view, name='salesman_view'),
    path('uploads_data/<int:id>/', views.uploads_data, name='uploads_data'),
    path('shipment/<int:id>/', views.shipment, name='shipment'),
    path('track_details/<int:id>/', views.track_details, name='track_details'),
   path('admin_return_request/', views.admin_return_request, name='admin_return_request'),
    path('supplier_return_request/', views.supplier_return_request, name='supplier_return_request'),
    path('admin_return_verify/<int:id>/', views.admin_return_verify, name='admin_return_verify'),
    path('supplier_return_complete/<int:id>/', views.supplier_return_complete, name='supplier_return_complete'),
    path('supplier_refund_complete/<int:id>/', views.supplier_refund_complete, name='supplier_refund_complete'),
    path('supplier_return_confirm/<int:id>/', views.supplier_return_confirm, name='supplier_return_confirm'),
    # path(' return_confirm_supplier/', views.return_confirm_supplier, name='return_confirm_supplier'),

    path('return_complete_supplier/', views.return_complete_supplier, name='return_complete_supplier'),

    path('refund_initiate_supplier/', views.refund_initiate_supplier, name='refund_initiate_supplier'),
    path('return_refund_complete/', views.return_refund_complete, name='return_refund_complete'),
    path('supplier_refund_initiate/<int:id>/', views.supplier_refund_initiate, name='supplier_refund_initiate'),







     path('view_added_mainagent/', views.view_added_mainagent, name='view_added_mainagent'),
    path('edit_mainagent/<int:id>/', views.edit_mainagent, name='edit_mainagent'),
    path('delete_mainagent/<int:id>/', views.delete_mainagent, name='delete_mainagent'),
    path('view_added_corporateagent/', views.view_added_corporateagent, name='view_added_corporateagent'),
    path('edit_corporateagent/<int:id>/', views.edit_corporateagent, name='edit_corporateagent'),
    path('delete_corporateagent/<int:id>/', views.delete_corporateagent, name='delete_corporateagent'),
     path('view_added_salesman/', views.view_added_salesman, name='view_added_salesman'),
    path('edit_salesman/<int:id>/', views.edit_salesman, name='edit_salesman'),
    path('delete_salesman/<int:id>/', views.delete_salesman, name='delete_salesman'),
    path('cancel_requested_orders/', views.cancel_requested_orders, name='cancel_requested_orders'),
   
    path('cancelled_order/<int:id>/', views.cancelled_order, name='cancelled_order'),
    path('supplier_cancel/<int:id>/', views.supplier_cancel, name='supplier_cancel'),

    path('cancel_request_from_admin/', views.cancel_request_from_admin, name='cancel_request_from_admin'),




    
    path('admin_verified_supplier_orders/', views.admin_verified_supplier_orders, name='admin_verified_supplier_orders'),

#new 

    


    


]