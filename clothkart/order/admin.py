from django.contrib import admin

# Register your models here.
from.models import Order,Payment,OrderProduct,Shipment,MainAgent,CorporateAgent,Supplier, Return,State,District,Salesman


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]



admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(Shipment)
admin.site.register(MainAgent)
admin.site.register(CorporateAgent)
admin.site.register(Return)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Salesman)







