from django.contrib import admin
from .models import Product,Contact,Orders,OrderUpdate
from django.contrib.admin.options import ModelAdmin


class ProductAdmin(ModelAdmin):
    list_display = ['category','type','brand','model','color','price']
    search_fields=  ['brand','model']
    list_filter = ['type']

class ContactAdmin(ModelAdmin):
     list_display = ['name','email','phone']

class OrdersAdmin(ModelAdmin):
     list_display = ['order_id','name','email','phone']

class OrderUpdateAdmin(ModelAdmin):
     list_display = ['order_id','update_desc','timestamp']


# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Orders,OrdersAdmin)
admin.site.register(OrderUpdate,OrderUpdateAdmin)